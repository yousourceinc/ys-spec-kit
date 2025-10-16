#!/usr/bin/env node

/**
 * Specify CLI - Node.js wrapper with OAuth authentication
 * This wraps the Python CLI and handles GitHub OAuth authentication
 */

const { authenticate, logout } = require('../src/auth/github-oauth');
const { spawn } = require('child_process');
const path = require('path');

async function main() {
  const args = process.argv.slice(2);
  
  // Handle logout command
  if (args[0] === 'logout') {
    logout();
    process.exit(0);
  }
  
  // Skip auth for help and version commands
  const skipAuthCommands = ['--help', '-h', '--version', '-v', 'help'];
  const needsAuth = args.length > 0 && !skipAuthCommands.some(cmd => args.includes(cmd));
  
  if (needsAuth) {
    try {
      // Authenticate with GitHub OAuth
      console.log('Verifying GitHub authentication...\n');
      await authenticate();
    } catch (error) {
      console.error('\n❌ Authentication failed:', error.message);
      console.error('\nPlease ensure you:');
      console.error('  1. Are a member of the required GitHub organization');
      console.error('  2. Have network access to github.com');
      console.error('  3. Have OAuth configured (see README.md)');
      console.error('\nFor help, visit: https://github.com/your-org/ys-spec-kit#oauth-setup\n');
      process.exit(1);
    }
  }
  
  // Run Python CLI
  runPythonCLI(args);
}

function runPythonCLI(args) {
  // Try to find Python 3
  const pythonCommands = ['python3', 'python'];
  let pythonCmd = 'python3';
  
  // Check which Python command is available
  for (const cmd of pythonCommands) {
    try {
      const result = require('child_process').spawnSync(cmd, ['--version'], { 
        stdio: 'pipe' 
      });
      if (result.status === 0) {
        pythonCmd = cmd;
        break;
      }
    } catch (e) {
      // Try next command
    }
  }
  
  const specify = spawn(pythonCmd, ['-m', 'specify_cli', ...args], {
    stdio: 'inherit',
    env: { ...process.env }
  });
  
  specify.on('close', (code) => {
    process.exit(code || 0);
  });
  
  specify.on('error', (error) => {
    if (error.code === 'ENOENT') {
      console.error('❌ Python 3 not found');
      console.error('Please install Python 3.11+ from https://python.org');
    } else {
      console.error('Error running Specify CLI:', error.message);
    }
    process.exit(1);
  });
}

// Run main function
main().catch(error => {
  console.error('Unexpected error:', error);
  process.exit(1);
});
