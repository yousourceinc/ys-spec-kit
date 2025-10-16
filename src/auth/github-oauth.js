#!/usr/bin/env node
/**
 * GitHub OAuth authentication for Specify CLI
 * Supports both browser flow (GUI) and device flow (headless/SSH)
 */

const http = require('http');
const { URL } = require('url');
const fs = require('fs');
const os = require('os');
const path = require('path');

// Try to load optional dependencies
let Octokit;
let open;
try {
  Octokit = require('@octokit/rest').Octokit;
  // open is a default export
  open = require('open').default || require('open');
} catch (e) {
  // Will be installed via npm
  console.warn('Warning: Some optional dependencies not installed:', e.message);
}

const CONFIG_DIR = path.join(os.homedir(), '.specify');
const TOKEN_FILE = path.join(CONFIG_DIR, 'oauth_token.json');

// OAuth configuration from environment variables
const OAUTH_CONFIG = {
  clientId: process.env.SPECIFY_GITHUB_CLIENT_ID || '',
  clientSecret: process.env.SPECIFY_GITHUB_CLIENT_SECRET || '',
  requiredOrg: process.env.SPECIFY_GITHUB_ORG || '',
  authUrl: 'https://github.com/login/oauth/authorize',
  tokenUrl: 'https://github.com/login/oauth/access_token',
  deviceCodeUrl: 'https://github.com/login/device/code',
  scopes: ['read:org', 'read:user'],
  redirectPort: parseInt(process.env.SPECIFY_OAUTH_PORT || '8888', 10)
};

/**
 * Main authentication function
 * Chooses between browser and device flow based on environment
 */
async function authenticate() {
  // Check for existing valid token
  const savedToken = loadSavedToken();
  if (savedToken && await validateToken(savedToken.access_token)) {
    console.log('✓ Using saved authentication');
    return savedToken.access_token;
  }
  
  console.log('🔐 Authenticating with GitHub...\n');
  
  // Check if OAuth is configured
  if (!OAUTH_CONFIG.clientId) {
    throw new Error(
      'GitHub OAuth not configured.\n' +
      'Set SPECIFY_GITHUB_CLIENT_ID and SPECIFY_GITHUB_CLIENT_SECRET environment variables.\n' +
      'See: https://github.com/your-org/ys-spec-kit#oauth-setup'
    );
  }
  
  // Detect if we should use device flow
  const isHeadless = !process.env.DISPLAY && process.platform !== 'win32' && process.platform !== 'darwin';
  const preferDevice = process.env.SPECIFY_DEVICE_FLOW === 'true';
  
  let token;
  if (isHeadless || preferDevice) {
    console.log('Using device flow (no browser required)');
    token = await authenticateDevice();
  } else {
    console.log('Using browser flow');
    token = await authenticateBrowser();
  }
  
  // Verify org membership
  if (OAUTH_CONFIG.requiredOrg) {
    if (!(await checkOrgMembership(token))) {
      throw new Error(`Not a member of required organization: ${OAUTH_CONFIG.requiredOrg}`);
    }
  }
  
  // Save token
  saveToken(token);
  console.log('✅ Authentication successful!\n');
  
  return token;
}

/**
 * Browser-based OAuth flow
 */
async function authenticateBrowser() {
  return new Promise((resolve, reject) => {
    const state = Math.random().toString(36).substring(7);
    
    // Create local callback server
    const server = http.createServer(async (req, res) => {
      const url = new URL(req.url, `http://localhost:${OAUTH_CONFIG.redirectPort}`);
      
      if (url.pathname === '/callback') {
        const code = url.searchParams.get('code');
        const returnedState = url.searchParams.get('state');
        
        // Verify state matches (CSRF protection)
        if (returnedState !== state) {
          res.writeHead(400, { 'Content-Type': 'text/html' });
          res.end('<h1>Authentication Failed</h1><p>State mismatch. Please try again.</p>');
          server.close();
          reject(new Error('State mismatch in OAuth flow'));
          return;
        }
        
        if (!code) {
          res.writeHead(400, { 'Content-Type': 'text/html' });
          res.end('<h1>Authentication Failed</h1><p>No authorization code received.</p>');
          server.close();
          reject(new Error('No authorization code received'));
          return;
        }
        
        try {
          // Exchange code for access token
          const token = await exchangeCodeForToken(code);
          
          res.writeHead(200, { 'Content-Type': 'text/html' });
          res.end(`
            <html>
              <head>
                <title>Authentication Successful</title>
                <style>
                  body { font-family: system-ui, -apple-system, sans-serif; text-align: center; padding: 50px; background: #f5f5f5; }
                  h1 { color: #24292e; }
                  .success { color: #28a745; font-size: 48px; }
                </style>
              </head>
              <body>
                <div class="success">✅</div>
                <h1>Authentication Successful!</h1>
                <p>You can close this window and return to your terminal.</p>
              </body>
            </html>
          `);
          
          server.close();
          resolve(token);
        } catch (error) {
          res.writeHead(500, { 'Content-Type': 'text/html' });
          res.end(`
            <html>
              <head><title>Authentication Failed</title></head>
              <body style="font-family: system-ui; text-align: center; padding: 50px;">
                <h1>❌ Authentication Failed</h1>
                <p>${escapeHtml(error.message)}</p>
              </body>
            </html>
          `);
          server.close();
          reject(error);
        }
      }
    });
    
    server.listen(OAUTH_CONFIG.redirectPort, () => {
      // Build authorization URL
      const authUrl = new URL(OAUTH_CONFIG.authUrl);
      authUrl.searchParams.append('client_id', OAUTH_CONFIG.clientId);
      authUrl.searchParams.append('redirect_uri', `http://localhost:${OAUTH_CONFIG.redirectPort}/callback`);
      authUrl.searchParams.append('scope', OAUTH_CONFIG.scopes.join(' '));
      authUrl.searchParams.append('state', state);
      
      console.log('Opening browser for authentication...');
      console.log('If browser doesn\'t open, visit:');
      console.log(authUrl.toString());
      console.log('');
      
      // Open browser
      if (open) {
        open(authUrl.toString()).catch(() => {
          console.log('Could not open browser automatically. Please open the URL manually.');
        });
      }
    });
    
    // Timeout after 5 minutes
    setTimeout(() => {
      server.close();
      reject(new Error('Authentication timeout (5 minutes)'));
    }, 5 * 60 * 1000);
  });
}

/**
 * Device flow OAuth (for SSH/headless environments)
 */
async function authenticateDevice() {
  // Step 1: Request device code
  const deviceCode = await requestDeviceCode();
  
  // Step 2: Show user code
  console.log('Please visit: \x1b[36m%s\x1b[0m', deviceCode.verification_uri);
  console.log('Enter code: \x1b[1m%s\x1b[0m\n', deviceCode.user_code);
  console.log('Waiting for authorization...');
  
  // Step 3: Poll for access token
  const token = await pollForAccessToken(deviceCode);
  
  return token;
}

/**
 * Request device code from GitHub
 */
async function requestDeviceCode() {
  const response = await fetch(OAUTH_CONFIG.deviceCodeUrl, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      client_id: OAUTH_CONFIG.clientId,
      scope: OAUTH_CONFIG.scopes.join(' ')
    })
  });
  
  if (!response.ok) {
    throw new Error(`Failed to request device code: ${response.statusText}`);
  }
  
  const data = await response.json();
  
  if (data.error) {
    throw new Error(`Device code error: ${data.error_description || data.error}`);
  }
  
  return data;
}

/**
 * Poll GitHub for access token after user authorizes
 */
async function pollForAccessToken(deviceCode) {
  const interval = deviceCode.interval * 1000; // Convert to ms
  const expiresAt = Date.now() + (deviceCode.expires_in * 1000);
  
  while (Date.now() < expiresAt) {
    await sleep(interval);
    
    const response = await fetch(OAUTH_CONFIG.tokenUrl, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        client_id: OAUTH_CONFIG.clientId,
        device_code: deviceCode.device_code,
        grant_type: 'urn:ietf:params:oauth:grant-type:device_code'
      })
    });
    
    const data = await response.json();
    
    if (data.access_token) {
      return data.access_token;
    }
    
    if (data.error === 'authorization_pending') {
      // Keep polling
      continue;
    }
    
    if (data.error === 'slow_down') {
      // Increase interval
      await sleep(5000);
      continue;
    }
    
    if (data.error) {
      throw new Error(`Authorization failed: ${data.error_description || data.error}`);
    }
  }
  
  throw new Error('Authorization timeout');
}

/**
 * Exchange authorization code for access token
 */
async function exchangeCodeForToken(code) {
  const response = await fetch(OAUTH_CONFIG.tokenUrl, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      client_id: OAUTH_CONFIG.clientId,
      client_secret: OAUTH_CONFIG.clientSecret,
      code: code,
      redirect_uri: `http://localhost:${OAUTH_CONFIG.redirectPort}/callback`
    })
  });
  
  if (!response.ok) {
    throw new Error(`Token exchange failed: ${response.statusText}`);
  }
  
  const data = await response.json();
  
  if (data.error) {
    throw new Error(`Token exchange error: ${data.error_description || data.error}`);
  }
  
  return data.access_token;
}

/**
 * Validate GitHub token
 */
async function validateToken(token) {
  try {
    if (!Octokit) {
      // Fallback validation via API
      const response = await fetch('https://api.github.com/user', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Accept': 'application/vnd.github.v3+json'
        }
      });
      return response.ok;
    }
    
    const octokit = new Octokit({ auth: token });
    await octokit.users.getAuthenticated();
    return true;
  } catch {
    return false;
  }
}

/**
 * Check if user is member of required organization
 */
async function checkOrgMembership(token) {
  try {
    if (!Octokit) {
      // Fallback check via API
      const response = await fetch('https://api.github.com/user/orgs', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Accept': 'application/vnd.github.v3+json'
        }
      });
      
      if (!response.ok) return false;
      
      const orgs = await response.json();
      return orgs.some(org => org.login === OAUTH_CONFIG.requiredOrg);
    }
    
    const octokit = new Octokit({ auth: token });
    const { data: orgs } = await octokit.orgs.listForAuthenticatedUser();
    return orgs.some(org => org.login === OAUTH_CONFIG.requiredOrg);
  } catch (error) {
    console.error('Error checking org membership:', error.message);
    return false;
  }
}

/**
 * Load saved token from disk
 */
function loadSavedToken() {
  try {
    if (fs.existsSync(TOKEN_FILE)) {
      const data = fs.readFileSync(TOKEN_FILE, 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {
    // Ignore errors, will re-authenticate
  }
  return null;
}

/**
 * Save token to disk
 */
function saveToken(token) {
  try {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
    fs.writeFileSync(TOKEN_FILE, JSON.stringify({
      access_token: token,
      created_at: new Date().toISOString()
    }, null, 2), { mode: 0o600 });
  } catch (error) {
    console.warn('Warning: Could not save token:', error.message);
  }
}

/**
 * Clear saved authentication
 */
function logout() {
  try {
    if (fs.existsSync(TOKEN_FILE)) {
      fs.unlinkSync(TOKEN_FILE);
      console.log('✅ Logged out successfully');
      return true;
    } else {
      console.log('No active session found');
      return false;
    }
  } catch (error) {
    console.error('Error during logout:', error.message);
    return false;
  }
}

/**
 * Utility: Sleep for ms milliseconds
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Utility: Escape HTML
 */
function escapeHtml(unsafe) {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// Export functions
module.exports = { 
  authenticate, 
  logout, 
  validateToken,
  checkOrgMembership
};

// Allow running as standalone script
if (require.main === module) {
  const command = process.argv[2];
  
  if (command === 'logout') {
    logout();
    process.exit(0);
  } else if (command === 'test') {
    authenticate()
      .then(() => {
        console.log('Authentication test successful');
        process.exit(0);
      })
      .catch(error => {
        console.error('Authentication test failed:', error.message);
        process.exit(1);
      });
  } else {
    console.log('Usage: node github-oauth.js [test|logout]');
    process.exit(1);
  }
}
