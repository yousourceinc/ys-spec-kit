<div align="center">
    <img src="./media/logo_small.webp"/>
    <h1>🌱 Spec Kit</h1>
    <h3><em>Build high-quality software faster.</em></h3>
</div>

<p align="center">
    <strong>An effort to allow organizations to focus on product scenarios rather than writing undifferentiated code with the help of Spec-Driven Development.</strong>
</p>

[![Release](https://github.com/github/spec-kit/actions/workflows/release.yml/badge.svg)](https://github.com/github/spec-kit/actions/workflows/release.yml)

---

## Table of Contents

- [🤔 What is Spec-Driven Development?](#-what-is-spec-driven-development)
- [⚡ Get started](#-get-started)
- [📽️ Video Overview](#️-video-overview)
- [🤖 Supported AI Agents](#-supported-ai-agents)
- [� GitHub OAuth Authentication](#-github-oauth-authentication)
- [�🔧 Specify CLI Reference](#-specify-cli-reference)
- [📚 Core philosophy](#-core-philosophy)
- [🌟 Development phases](#-development-phases)
- [🎯 Experimental goals](#-experimental-goals)
- [🔧 Prerequisites](#-prerequisites)
- [📖 Learn more](#-learn-more)
- [📋 Detailed process](#-detailed-process)
- [🔍 Troubleshooting](#-troubleshooting)
- [👥 Maintainers](#-maintainers)
- [💬 Support](#-support)
- [🙏 Acknowledgements](#-acknowledgements)
- [📄 License](#-📄-license)

## 🤔 What is Spec-Driven Development?

Spec-Driven Development **flips the script** on traditional software development. For decades, code has been king — specifications were just scaffolding we built and discarded once the "real work" of coding began. Spec-Driven Development changes this: **specifications become executable**, directly generating working implementations rather than just guiding them.

## ⚡ Get started

### 1. Install Specify

Choose your preferred installation method:

#### Option 1: npm Installation (Recommended for Teams with OAuth)

Install via npm with automatic GitHub OAuth authentication:

```bash
npm install -g @your-org/specify-cli
```

Then use the tool directly:

```bash
specify init <PROJECT_NAME>
specify check
```

**This option includes:**
- Automatic GitHub OAuth authentication
- Team access control
- Pre-configured organization verification
- Works in terminal environments (both GUI and SSH)

#### Option 2: uv Installation (Traditional Persistent)

Install once and use everywhere:

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

Then use the tool directly:

```bash
specify init <PROJECT_NAME>
specify check
```

#### Option 3: One-time Usage with uv

Run directly without installing:

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>
```

**Benefits of persistent installation:**

- Tool stays installed and available in PATH
- No need to create shell aliases
- Better tool management with `uv tool list`, `uv tool upgrade`, `uv tool uninstall`
- Cleaner shell configuration

### 2. Establish project principles

Use the **`/constitution`** command to create your project's governing principles and development guidelines that will guide all subsequent development.

```bash
/constitution Create principles focused on code quality, testing standards, user experience consistency, and performance requirements
```

### 3. Create the spec

Use the **`/specify`** command to describe what you want to build. Focus on the **what** and **why**, not the tech stack.

```bash
/specify Build an application that can help me organize my photos in separate photo albums. Albums are grouped by date and can be re-organized by dragging and dropping on the main page. Albums are never in other nested albums. Within each album, photos are previewed in a tile-like interface.
```

### 4. Create a technical implementation plan

Use the **`/plan`** command to provide your tech stack and architecture choices.

```bash
/plan The application uses Vite with minimal number of libraries. Use vanilla HTML, CSS, and JavaScript as much as possible. Images are not uploaded anywhere and metadata is stored in a local SQLite database.
```

### 5. Break down into tasks

Use **`/tasks`** to create an actionable task list from your implementation plan.

```bash
/tasks
```

### 6. Execute implementation

Use **`/implement`** to execute all tasks and build your feature according to the plan.

```bash
/implement
```

For detailed step-by-step instructions, see our [comprehensive guide](./spec-driven.md).

## 📽️ Video Overview

Want to see Spec Kit in action? Watch our [video overview](https://www.youtube.com/watch?v=a9eR1xsfvHg&pp=0gcJCckJAYcqIYzv)!

[![Spec Kit video header](/media/spec-kit-video-header.jpg)](https://www.youtube.com/watch?v=a9eR1xsfvHg&pp=0gcJCckJAYcqIYzv)

## 🤖 Supported AI Agents

| Agent                                                     | Support | Notes                                             |
|-----------------------------------------------------------|---------|---------------------------------------------------|
| [Claude Code](https://www.anthropic.com/claude-code)      | ✅ |                                                   |
| [GitHub Copilot](https://code.visualstudio.com/)          | ✅ |                                                   |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | ✅ |                                                   |
| [Cursor](https://cursor.sh/)                              | ✅ |                                                   |
| [Qwen Code](https://github.com/QwenLM/qwen-code)          | ✅ |                                                   |
| [opencode](https://opencode.ai/)                          | ✅ |                                                   |
| [Windsurf](https://windsurf.com/)                         | ✅ |                                                   |
| [Kilo Code](https://github.com/Kilo-Org/kilocode)         | ✅ |                                                   |
| [Auggie CLI](https://docs.augmentcode.com/cli/overview)   | ✅ |                                                   |
| [Roo Code](https://roocode.com/)                          | ✅ |                                                   |
| [Amazon Q Developer CLI](https://aws.amazon.com/developer/learning/q-developer-cli/) | ⚠️ | Amazon Q Developer CLI [does not support](https://github.com/aws/amazon-q-developer-cli/issues/3064) custom arguments for slash commands. |
| [Codex CLI](https://github.com/openai/codex)              | ⚠️ | Codex [does not support](https://github.com/openai/codex/issues/2890) custom arguments for slash commands.  |

## 🎯 Division-Aware Workflows

Specify CLI supports **division-aware development workflows** that prioritize implementation guides based on your development focus area. This ensures AI agents receive the most relevant guidance for your specific domain.

### Available Divisions

| Division   | Focus Area | Description |
|------------|------------|-------------|
| **SE**     | Software Engineering | Backend development, APIs, web applications, system architecture |
| **DS**     | Data Science | Data analysis, machine learning, statistical modeling, data pipelines |
| **Platform**| Platform Engineering | Infrastructure, DevOps, cloud architecture, containerization |

### How Division-Aware Workflows Work

1. **Guide Prioritization**: When you specify a division during project initialization, guides are prioritized in this order:
   - **Primary**: Guides specific to your division (e.g., SE division gets backend/API guides first)
   - **Common**: Cross-cutting guides applicable to all divisions (e.g., Git workflow, testing)
   - **Other**: Guides from other divisions (available as reference)

2. **AI Context Updates**: Agent context files are automatically updated with division-specific guide references, ensuring your AI assistant has access to the most relevant implementation patterns.

3. **Dynamic Updates**: As you work on features, the `update-agent-context.sh` script reads your project's division and refreshes guide priorities accordingly.

### Division Examples

```bash
# Backend API development (Software Engineering focus)
specify init api-service --ai claude --division SE

# Data pipeline project (Data Science focus)
specify init data-pipeline --ai copilot --division DS

# Infrastructure automation (Platform focus)
specify init infra-automation --ai cursor --division Platform
```

### Benefits

- **Relevant Guidance**: AI agents receive domain-specific implementation patterns
- **Faster Development**: Less time spent filtering irrelevant guides
- **Consistent Practices**: Division-specific best practices are prioritized
- **Team Alignment**: Different teams can focus on their domain expertise

## 🔐 GitHub OAuth Authentication

Specify CLI can be configured with GitHub OAuth for team access control and secure distribution. This is especially useful for organizations that want to:

- **Control team access** - Verify organization membership automatically
- **Secure distribution** - Distribute Specify CLI via npm with built-in authentication
- **Support multiple environments** - Works in both GUI (browser-based) and SSH/headless (device code flow) environments
- **Manage credentials safely** - Tokens stored securely with restricted file permissions

### OAuth Setup

For detailed OAuth setup instructions, see [OAuth Setup Guide](./docs/OAUTH_SETUP.md).

**For Teams:** See [Team Installation Guide](./docs/TEAM_INSTALLATION.md) for complete onboarding instructions.

## 🔧 Specify CLI Reference

The `specify` command supports the following options:

### Commands

| Command     | Description                                                    |
|-------------|----------------------------------------------------------------|
| `init`      | Initialize a new Specify project from the latest template      |
| `check`     | Check for installed tools (`git`, `claude`, `gemini`, `code`/`code-insiders`, `cursor-agent`, `windsurf`, `qwen`, `opencode`, `codex`) |
| `logout`    | Clear GitHub OAuth authentication and remove stored token      |
| `guides update` | Update implementation guides to the latest version using git submodule |

### `specify init` Arguments & Options

| Argument/Option        | Type     | Description                                                                  |
|------------------------|----------|------------------------------------------------------------------------------|
| `<project-name>`       | Argument | Name for your new project directory (optional if using `--here`, or use `.` for current directory) |
| `--ai`                 | Option   | AI assistant to use: `claude`, `gemini`, `copilot`, `cursor`, `qwen`, `opencode`, `codex`, `windsurf`, `kilocode`, `auggie`, `roo`, or `q` |
| `--division`           | Option   | Development division for guide prioritization: `SE` (Software Engineering), `DS` (Data Science), or `Platform` |
| `--script`             | Option   | Script variant to use: `sh` (bash/zsh) or `ps` (PowerShell)                 |
| `--ignore-agent-tools` | Flag     | Skip checks for AI agent tools like Claude Code                             |
| `--no-git`             | Flag     | Skip git repository initialization                                          |
| `--here`               | Flag     | Initialize project in the current directory instead of creating a new one   |
| `--force`              | Flag     | Force merge/overwrite when initializing in current directory (skip confirmation) |
| `--skip-tls`           | Flag     | Skip SSL/TLS verification (not recommended)                                 |
| `--debug`              | Flag     | Enable detailed debug output for troubleshooting                            |

### Examples

```bash
# Basic project initialization
specify init my-project

# Initialize with specific AI assistant
specify init my-project --ai claude

# Initialize with division for guide prioritization
specify init my-project --ai claude --division SE
specify init my-project --ai copilot --division DS
specify init my-project --ai cursor --division Platform

# Initialize with Cursor support
specify init my-project --ai cursor

# Initialize with Windsurf support
specify init my-project --ai windsurf

# Initialize with PowerShell scripts (Windows/cross-platform)
specify init my-project --ai copilot --script ps

# Initialize in current directory
specify init . --ai copilot
# or use the --here flag
specify init --here --ai copilot

# Force merge into current (non-empty) directory without confirmation
specify init . --force --ai copilot
# or 
specify init --here --force --ai copilot

# Skip git initialization
specify init my-project --ai gemini --no-git

# Enable debug output for troubleshooting
specify init my-project --ai claude --debug

# Check system requirements
specify check
```

### Available Slash Commands

After running `specify init`, your AI coding agent will have access to these slash commands for structured development:

| Command         | Description                                                           |
|-----------------|-----------------------------------------------------------------------|
| `/constitution` | Create or update project governing principles and development guidelines |
| `/specify`      | Define what you want to build (requirements and user stories)        |
| `/clarify`      | Clarify underspecified areas (must be run before `/plan` unless explicitly skipped; formerly `/quizme`) |
| `/plan`         | Create technical implementation plans with your chosen tech stack     |
| `/tasks`        | Generate actionable task lists for implementation                     |
| `/analyze`      | Cross-artifact consistency & coverage analysis (run after /tasks, before /implement) |
| `/implement`    | Execute all tasks to build the feature according to the plan         |

### Guides Management (CLI)

Manage implementation guides for your project:

```bash
# Update guides to the latest version
specify guides update
```

**Planned commands** (not yet implemented):
```bash
# Search for guides by keyword (coming soon)
specify guides search <keyword>

# Display a specific guide (coming soon)
specify guides show <guide-path>
```

**Setup**: Guide repository is configured at the system level via the `SPECIFY_GUIDES_REPO_URL` environment variable before running `specify init`. Set this variable to automatically integrate implementation guides:

```bash
# Example: Set guides repository URL
export SPECIFY_GUIDES_REPO_URL="git@github.com:your-org/implementation-guides.git"

# Initialize project (guides will be cloned automatically)
specify init my-project --ai claude
```

**Note**: Guide repository configuration (add/remove) is handled at the binary/system level and cannot be modified by developers at runtime. Developers can only update existing guides to the latest version.

### Governance Layer

The Specify CLI includes a **governance layer** for managing compliance, waivers, and rule validation across your project:

#### Compliance Checking

Run compliance checks against your implementation guides to ensure adherence to defined rules:

```bash
specify check-compliance [--guides GUIDE_PATHS] [--no-cache]
```

**Features:**
- Discover and evaluate rules from implementation guides
- Cross-reference with active waivers
- Generate compliance reports with detailed metrics
- Performance metrics tracking (rule evaluation times, total duration)
- Guide caching for large codebases (1-hour expiry)

#### Waiver Management

Create and manage compliance exceptions with full audit trail:

```bash
# Create a new waiver
specify waive-requirement "Reason for exception" [--rules RULE_IDS]

# List all active waivers
specify waivers list [--verbose]

# View details for a specific waiver
specify waivers show W-001
```

**Features:**
- Version-controlled waiver storage (`.specify/waivers.md`)
- Immutable audit trail with timestamps
- Division-aware waiver tracking
- Rich console formatting for waiver display

#### Rule Authoring

Define compliance rules in your implementation guides using YAML frontmatter:

```markdown
---
rules:
  - id: "RULE-001"
    type: "file_exists"
    path: "src/index.js"
    division: "SE"
    description: "Ensure main entry point exists"
  
  - id: "RULE-002"
    type: "text_includes"
    target: "package.json"
    text: '"scripts"'
    description: "Ensure npm scripts defined"
---

# My Implementation Guide
```

**Supported rule types:**
- `file_exists`: Verify required files are present
- `dependency_present`: Check for required dependencies
- `text_includes`: Validate text content in files

For detailed governance layer documentation and quickstart guide, see [Governance Layer Quickstart](./docs/governance-quickstart.md).

### Environment Variables

| Variable         | Description                                                                                    |
|------------------|------------------------------------------------------------------------------------------------|
| `SPECIFY_FEATURE` | Override feature detection for non-Git repositories. Set to the feature directory name (e.g., `001-photo-albums`) to work on a specific feature when not using Git branches.<br/>**Must be set in the context of the agent you're working with prior to using `/plan` or follow-up commands. |
| `SPECIFY_GUIDES_REPO_URL` | **System-level configuration** for automatic implementation guides integration. Set to a Git repository URL (e.g., `git@github.com:your-org/implementation-guides.git`) before running `specify init`. When set, this environment variable overrides the default hardcoded guides repository URL. When not set or empty, falls back to the default implementation guides repository. Guides will be automatically cloned as a git submodule into `context/references/`. |

## 📚 Core philosophy

Spec-Driven Development is a structured process that emphasizes:

- **Intent-driven development** where specifications define the "_what_" before the "_how_"
- **Rich specification creation** using guardrails and organizational principles
- **Multi-step refinement** rather than one-shot code generation from prompts
- **Heavy reliance** on advanced AI model capabilities for specification interpretation

## �️ Product Life Cycle Framework

The product life cycle and associated maturity framework typically refer to key stages that a product passes through, from inception to withdrawal from the market. The most widely recognized frameworks break these down into four or five primary levels: development (optional), introduction, growth, maturity, and decline.[1][2][3]

### Primary Product Life Cycle Stages

| Stage         | Description                                                                                                      |
|---------------|------------------------------------------------------------------------------------------------------------------|
| Development   | Product is being designed and tested before entering the market (sometimes not considered a public phase)[3]. |
| Introduction  | Product is launched, sales are low, and marketing focuses on building awareness and adoption[4][5].       |
| Growth        | Sales accelerate, market acceptance grows, and competition increases as rivals enter the space[2][4].     |
| Maturity      | Market saturation occurs, growth slows, competition peaks, and emphasis shifts to defending market share[6][4]. |
| Decline       | Sales decline due to market saturation, technological changes, or shifting consumer preferences[6][4].     |

### Maturity Framework Connection

A maturity framework for a product means defining and measuring the specific attributes or capabilities a product achieves as it moves through these phases. In the maturity stage:
- The product is widely recognized and adopted by the target market.
- Sales plateau, and competition is at its most intense.
- Cost-control, incremental innovation, and market differentiation are primary strategies.
- Businesses may release product extensions, target new segments, or find efficiency improvements to stay competitive.[7][4]

### Stages in Detail

- **Introduction:** Focus is on education and awareness due to newness in the market; investment is high, and profitability is limited.[5][4]
- **Growth:** Rapid adoption, increased market share, and attempts to outpace competitors by refining features or marketing.[2][5]
- **Maturity:** The product's market penetration peaks, sales are stable, and the business shifts from expanding reach to maximizing efficiency and differentiation.[6][4][7]
- **Decline:** Sales and relevance decrease; the company may retire the product, pivot, or seek to reinvent it.[4][6]

### Key Framework Takeaways

- The stages guide resource allocation, marketing, product improvement, and portfolio management.[3][4]
- Proactively recognizing the current stage helps companies implement changes, avoid premature decline, and maximize a product's profitability.[7][4]

This cyclical maturity model is foundational in business and product management disciplines, ensuring product teams tailor strategies to the current lifecycle phase for optimal outcomes.[2][3][7]

## �🌟 Development phases

| Phase | Focus | Key Activities |
|-------|-------|----------------|
| **0-to-1 Development** ("Greenfield") | Generate from scratch | <ul><li>Start with high-level requirements</li><li>Generate specifications</li><li>Plan implementation steps</li><li>Build production-ready applications</li></ul> |
| **Creative Exploration** | Parallel implementations | <ul><li>Explore diverse solutions</li><li>Support multiple technology stacks & architectures</li><li>Experiment with UX patterns</li></ul> |
| **Iterative Enhancement** ("Brownfield") | Brownfield modernization | <ul><li>Add features iteratively</li><li>Modernize legacy systems</li><li>Adapt processes</li></ul> |

## 🎯 Experimental goals

Our research and experimentation focus on:

### Technology independence

- Create applications using diverse technology stacks
- Validate the hypothesis that Spec-Driven Development is a process not tied to specific technologies, programming languages, or frameworks

### Enterprise constraints

- Demonstrate mission-critical application development
- Incorporate organizational constraints (cloud providers, tech stacks, engineering practices)
- Support enterprise design systems and compliance requirements

### User-centric development

- Build applications for different user cohorts and preferences
- Support various development approaches (from vibe-coding to AI-native development)

### Creative & iterative processes

- Validate the concept of parallel implementation exploration
- Provide robust iterative feature development workflows
- Extend processes to handle upgrades and modernization tasks

## 🔧 Prerequisites

- **Linux/macOS** (or WSL2 on Windows)
- AI coding agent: [Claude Code](https://www.anthropic.com/claude-code), [GitHub Copilot](https://code.visualstudio.com/), [Gemini CLI](https://github.com/google-gemini/gemini-cli), [Cursor](https://cursor.sh/), [Qwen CLI](https://github.com/QwenLM/qwen-code), [opencode](https://opencode.ai/), [Codex CLI](https://github.com/openai/codex), [Windsurf](https://windsurf.com/), or [Amazon Q Developer CLI](https://aws.amazon.com/developer/learning/q-developer-cli/)
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [Node.js 16+](https://nodejs.org/) (required for npm distribution with OAuth authentication)
- [uv](https://docs.astral.sh/uv/) for package management (optional, only needed for `uv` installation method)

If you encounter issues with an agent, please open an issue so we can refine the integration.

## 📖 Learn more

- **[Complete Spec-Driven Development Methodology](./spec-driven.md)** - Deep dive into the full process
- **[Detailed Walkthrough](#-detailed-process)** - Step-by-step implementation guide

---

## 📋 Detailed process

<details>
<summary>Click to expand the detailed step-by-step walkthrough</summary>

You can use the Specify CLI to bootstrap your project, which will bring in the required artifacts in your environment. Run:

```bash
specify init <project_name>
```

Or initialize in the current directory:

```bash
specify init .
# or use the --here flag
specify init --here
# Skip confirmation when the directory already has files
specify init . --force
# or
specify init --here --force
```

![Specify CLI bootstrapping a new project in the terminal](./media/specify_cli.gif)

You will be prompted to select the AI agent you are using. You can also proactively specify it directly in the terminal:

```bash
specify init <project_name> --ai claude
specify init <project_name> --ai gemini
specify init <project_name> --ai copilot
specify init <project_name> --ai cursor
specify init <project_name> --ai qwen
specify init <project_name> --ai opencode
specify init <project_name> --ai codex
specify init <project_name> --ai windsurf
specify init <project_name> --ai q
# Or in current directory:
specify init . --ai claude
specify init . --ai codex
# or use --here flag
specify init --here --ai claude
specify init --here --ai codex
# Force merge into a non-empty current directory
specify init . --force --ai claude
# or
specify init --here --force --ai claude
```

The CLI will check if you have Claude Code, Gemini CLI, Cursor CLI, Qwen CLI, opencode, Codex CLI, or Amazon Q Developer CLI installed. If you do not, or you prefer to get the templates without checking for the right tools, use `--ignore-agent-tools` with your command:

```bash
specify init <project_name> --ai claude --ignore-agent-tools
```

### **STEP 1:** Establish project principles

Go to the project folder and run your AI agent. In our example, we're using `claude`.

![Bootstrapping Claude Code environment](./media/bootstrap-claude-code.gif)

You will know that things are configured correctly if you see the `/constitution`, `/specify`, `/plan`, `/tasks`, and `/implement` commands available.

The first step should be establishing your project's governing principles using the `/constitution` command. This helps ensure consistent decision-making throughout all subsequent development phases:

```text
/constitution Create principles focused on code quality, testing standards, user experience consistency, and performance requirements. Include governance for how these principles should guide technical decisions and implementation choices.
```

This step creates or updates the `.specify/memory/constitution.md` file with your project's foundational guidelines that the AI agent will reference during specification, planning, and implementation phases.

### **STEP 2:** Create project specifications

With your project principles established, you can now create the functional specifications. Use the `/specify` command and then provide the concrete requirements for the project you want to develop.

>[!IMPORTANT]
>Be as explicit as possible about _what_ you are trying to build and _why_. **Do not focus on the tech stack at this point**.

An example prompt:

```text
Develop Taskify, a team productivity platform. It should allow users to create projects, add team members,
assign tasks, comment and move tasks between boards in Kanban style. In this initial phase for this feature,
let's call it "Create Taskify," let's have multiple users but the users will be declared ahead of time, predefined.
I want five users in two different categories, one product manager and four engineers. Let's create three
different sample projects. Let's have the standard Kanban columns for the status of each task, such as "To Do,"
"In Progress," "In Review," and "Done." There will be no login for this application as this is just the very
first testing thing to ensure that our basic features are set up. For each task in the UI for a task card,
you should be able to change the current status of the task between the different columns in the Kanban work board.
You should be able to leave an unlimited number of comments for a particular card. You should be able to, from that task
card, assign one of the valid users. When you first launch Taskify, it's going to give you a list of the five users to pick
from. There will be no password required. When you click on a user, you go into the main view, which displays the list of
projects. When you click on a project, you open the Kanban board for that project. You're going to see the columns.
You'll be able to drag and drop cards back and forth between different columns. You will see any cards that are
assigned to you, the currently logged in user, in a different color from all the other ones, so you can quickly
see yours. You can edit any comments that you make, but you can't edit comments that other people made. You can
delete any comments that you made, but you can't delete comments anybody else made.
```

After this prompt is entered, you should see Claude Code kick off the planning and spec drafting process. Claude Code will also trigger some of the built-in scripts to set up the repository.

Once this step is completed, you should have a new branch created (e.g., `001-create-taskify`), as well as a new specification in the `specs/001-create-taskify` directory.

The produced specification should contain a set of user stories and functional requirements, as defined in the template.

At this stage, your project folder contents should resemble the following:

```text
└── .specify
    ├── memory
    │	 └── constitution.md
    ├── scripts
    │	 ├── check-prerequisites.sh
    │	 ├── common.sh
    │	 ├── create-new-feature.sh
    │	 ├── setup-plan.sh
    │	 └── update-claude-md.sh
    ├── specs
    │	 └── 001-create-taskify
    │	     └── spec.md
    └── templates
        ├── plan-template.md
        ├── spec-template.md
        └── tasks-template.md
```

### **STEP 3:** Functional specification clarification (required before planning)

With the baseline specification created, you can go ahead and clarify any of the requirements that were not captured properly within the first shot attempt.

You should run the structured clarification workflow **before** creating a technical plan to reduce rework downstream.

Preferred order:
1. Use `/clarify` (structured) – sequential, coverage-based questioning that records answers in a Clarifications section.
2. Optionally follow up with ad-hoc free-form refinement if something still feels vague.

If you intentionally want to skip clarification (e.g., spike or exploratory prototype), explicitly state that so the agent doesn't block on missing clarifications.

Example free-form refinement prompt (after `/clarify` if still needed):

```text
For each sample project or project that you create there should be a variable number of tasks between 5 and 15
tasks for each one randomly distributed into different states of completion. Make sure that there's at least
one task in each stage of completion.
```

You should also ask Claude Code to validate the **Review & Acceptance Checklist**, checking off the things that are validated/pass the requirements, and leave the ones that are not unchecked. The following prompt can be used:

```text
Read the review and acceptance checklist, and check off each item in the checklist if the feature spec meets the criteria. Leave it empty if it does not.
```

It's important to use the interaction with Claude Code as an opportunity to clarify and ask questions around the specification - **do not treat its first attempt as final**.

### **STEP 4:** Generate a plan

You can now be specific about the tech stack and other technical requirements. You can use the `/plan` command that is built into the project template with a prompt like this:

```text
We are going to generate this using .NET Aspire, using Postgres as the database. The frontend should use
Blazor server with drag-and-drop task boards, real-time updates. There should be a REST API created with a projects API,
tasks API, and a notifications API.
```

The output of this step will include a number of implementation detail documents, with your directory tree resembling this:

```text
.
├── CLAUDE.md
├── memory
│	 └── constitution.md
├── scripts
│	 ├── check-prerequisites.sh
│	 ├── common.sh
│	 ├── create-new-feature.sh
│	 ├── setup-plan.sh
│	 └── update-claude-md.sh
├── specs
│	 └── 001-create-taskify
│	     ├── contracts
│	     │	 ├── api-spec.json
│	     │	 └── signalr-spec.md
│	     ├── data-model.md
│	     ├── plan.md
│	     ├── quickstart.md
│	     ├── research.md
│	     └── spec.md
└── templates
    ├── CLAUDE-template.md
    ├── plan-template.md
    ├── spec-template.md
    └── tasks-template.md
```

Check the `research.md` document to ensure that the right tech stack is used, based on your instructions. You can ask Claude Code to refine it if any of the components stand out, or even have it check the locally-installed version of the platform/framework you want to use (e.g., .NET).

Additionally, you might want to ask Claude Code to research details about the chosen tech stack if it's something that is rapidly changing (e.g., .NET Aspire, JS frameworks), with a prompt like this:

```text
I want you to go through the implementation plan and implementation details, looking for areas that could
benefit from additional research as .NET Aspire is a rapidly changing library. For those areas that you identify that
require further research, I want you to update the research document with additional details about the specific
versions that we are going to be using in this Taskify application and spawn parallel research tasks to clarify
any details using research from the web.
```

During this process, you might find that Claude Code gets stuck researching the wrong thing - you can help nudge it in the right direction with a prompt like this:

```text
I think we need to break this down into a series of steps. First, identify a list of tasks
that you would need to do during implementation that you're not sure of or would benefit
from further research. Write down a list of those tasks. And then for each one of these tasks,
I want you to spin up a separate research task so that the net results is we are researching
all of those very specific tasks in parallel. What I saw you doing was it looks like you were
researching .NET Aspire in general and I don't think that's gonna do much for us in this case.
That's way too untargeted research. The research needs to help you solve a specific targeted question.
```

>[!NOTE]
>Claude Code might be over-eager and add components that you did not ask for. Ask it to clarify the rationale and the source of the change.

### **STEP 5:** Have Claude Code validate the plan

With the plan in place, you should have Claude Code run through it to make sure that there are no missing pieces. You can use a prompt like this:

```text
Now I want you to go and audit the implementation plan and the implementation detail files.
Read through it with an eye on determining whether or not there is a sequence of tasks that you need
to be doing that are obvious from reading this. Because I don't know if there's enough here. For example,
when I look at the core implementation, it would be useful to reference the appropriate places in the implementation
details where it can find the information as it walks through each step in the core implementation or in the refinement.
```

This helps refine the implementation plan and helps you avoid potential blind spots that Claude Code missed in its planning cycle. Once the initial refinement pass is complete, ask Claude Code to go through the checklist once more before you can get to the implementation.

You can also ask Claude Code (if you have the [GitHub CLI](https://docs.github.com/en/github-cli/github-cli) installed) to go ahead and create a pull request from your current branch to `main` with a detailed description, to make sure that the effort is properly tracked.

>[!NOTE]
>Before you have the agent implement it, it's also worth prompting Claude Code to cross-check the details to see if there are any over-engineered pieces (remember - it can be over-eager). If over-engineered components or decisions exist, you can ask Claude Code to resolve them. Ensure that Claude Code follows the [constitution](base/memory/constitution.md) as the foundational piece that it must adhere to when establishing the plan.

### STEP 6: Implementation

Once ready, use the `/implement` command to execute your implementation plan:

```text
/implement
```

The `/implement` command will:
- Validate that all prerequisites are in place (constitution, spec, plan, and tasks)
- Parse the task breakdown from `tasks.md`
- Execute tasks in the correct order, respecting dependencies and parallel execution markers
- Follow the TDD approach defined in your task plan
- Provide progress updates and handle errors appropriately

>[!IMPORTANT]
>The AI agent will execute local CLI commands (such as `dotnet`, `npm`, etc.) - make sure you have the required tools installed on your machine.

Once the implementation is complete, test the application and resolve any runtime errors that may not be visible in CLI logs (e.g., browser console errors). You can copy and paste such errors back to your AI agent for resolution.

</details>

---

## 🔍 Troubleshooting

### Git Credential Manager on Linux

If you're having issues with Git authentication on Linux, you can install Git Credential Manager:

```bash
#!/usr/bin/env bash
set -e
echo "Downloading Git Credential Manager v2.6.1..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "Installing Git Credential Manager..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "Configuring Git to use GCM..."
git config --global credential.helper manager
echo "Cleaning up..."
rm gcm-linux_amd64.2.6.1.deb
```

## 👥 Maintainers

- Den Delimarsky ([@localden](https://github.com/localden))
- John Lam ([@jflam](https://github.com/jflam))

## 💬 Support

For support, please open a [GitHub issue](https://github.com/github/spec-kit/issues/new). We welcome bug reports, feature requests, and questions about using Spec-Driven Development.

## 🙏 Acknowledgements

This project is heavily influenced by and based on the work and research of [John Lam](https://github.com/jflam).

## 📄 License

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](./LICENSE) file for the full terms.
