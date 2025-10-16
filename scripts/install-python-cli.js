#!/usr/bin/env node
/**
 * Post-install script to set up Python CLI
 */

const { execSync, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🔧 Setting up Specify CLI...\n');

// Check for Python 3
const pythonCommands = ['python3', 'python'];
let pythonCmd = null;
let pythonVersion = null;

for (const cmd of pythonCommands) {
  try {
    const result = spawnSync(cmd, ['--version'], { encoding: 'utf8' });
    if (result.status === 0) {
      pythonCmd = cmd;
      pythonVersion = result.stdout || result.stderr;
      break;
    }
  } catch (error) {
    // Try next command
  }
}

if (!pythonCmd) {
  console.error('❌ Python 3 is required but not found');
  console.error('Install Python 3.11+ from https://python.org');
  process.exit(1);
}

console.log(`✓ Found ${pythonVersion.trim()}`);

// Check Python version
try {
  const versionCheck = spawnSync(pythonCmd, [
    '-c', 
    'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)'
  ]);
  
  if (versionCheck.status !== 0) {
    console.error('❌ Python 3.11 or higher is required');
    console.error('Current version:', pythonVersion.trim());
    process.exit(1);
  }
} catch (error) {
  console.warn('⚠️  Could not verify Python version');
}

console.log('📦 Installing Python CLI...\n');

try {
  // Get the repository root (parent of node_modules)
  const repoRoot = path.resolve(__dirname, '..');
  
  // Check if we're in development mode (has pyproject.toml)
  const isDev = fs.existsSync(path.join(repoRoot, 'pyproject.toml'));
  
  if (isDev) {
    console.log('Development mode: Installing from local source');
    // Install in editable mode for development
    execSync(`${pythonCmd} -m pip install -e "${repoRoot}"`, {
      stdio: 'inherit',
      cwd: repoRoot
    });
  } else {
    // Production: Install from git
    console.log('Production mode: Installing from git repository');
    const gitUrl = 'git+https://github.com/your-org/ys-spec-kit.git@main';
    execSync(`${pythonCmd} -m pip install --user "${gitUrl}"`, {
      stdio: 'inherit'
    });
  }
  
  console.log('\n✅ Specify CLI installed successfully');
  console.log('\nNext steps:');
  console.log('  1. Set up GitHub OAuth (see README.md)');
  console.log('  2. Run: specify init my-project --ai claude');
  
} catch (error) {
  console.error('\n❌ Installation failed:', error.message);
  console.error('\nTry manual installation:');
  console.error(`  ${pythonCmd} -m pip install --user git+https://github.com/your-org/ys-spec-kit.git@main`);
  process.exit(1);
}
