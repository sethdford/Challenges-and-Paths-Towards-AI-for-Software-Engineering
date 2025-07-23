"""
Claude Code Integration System

Custom commands, hooks, and tools for seamless AI-SWE workflows
with Claude as the primary AI coding assistant.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable, Union
import json
import asyncio
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class CommandCategory(Enum):
    """Categories of Claude Code commands"""
    TASK_ANALYSIS = "task_analysis"
    CODE_GENERATION = "code_generation" 
    CODE_TRANSFORMATION = "code_transformation"
    TESTING_VERIFICATION = "testing_verification"
    MAINTENANCE = "maintenance"
    SCAFFOLDING = "scaffolding"
    COLLABORATION = "collaboration"
    EVALUATION = "evaluation"

class ExecutionMode(Enum):
    """Execution modes for Claude commands"""
    INTERACTIVE = "interactive"    # Requires human confirmation
    SEMI_AUTO = "semi_auto"       # Auto with human oversight
    AUTONOMOUS = "autonomous"     # Fully automated

class ToolIntegration(Enum):
    """External tool integrations"""
    IDE = "ide"                   # IDE integration (VS Code, Cursor)
    TERMINAL = "terminal"         # Terminal/shell access
    GIT = "git"                   # Git operations
    CI_CD = "ci_cd"              # CI/CD pipelines
    STATIC_ANALYSIS = "static_analysis"  # Linters, type checkers
    TESTING = "testing"           # Test frameworks
    DOCUMENTATION = "documentation"     # Doc generators
    DEPLOYMENT = "deployment"     # Deployment tools

@dataclass
class CommandContext:
    """Context for command execution"""
    workspace_path: Path
    current_files: List[str]
    git_branch: Optional[str] = None
    project_type: Optional[str] = None
    language: Optional[str] = None
    frameworks: List[str] = field(default_factory=list)
    recent_changes: List[str] = field(default_factory=list)
    user_preferences: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ClaudeCommand:
    """Represents a Claude Code command"""
    name: str
    category: CommandCategory
    description: str
    usage_pattern: str
    parameters: Dict[str, Any]
    execution_mode: ExecutionMode
    required_tools: List[ToolIntegration]
    addressed_tasks: List[str]
    implementation: Optional[Callable] = None
    
    def __str__(self) -> str:
        return f"/{self.name}: {self.description}"

class ClaudeHook:
    """Event hooks for Claude integration"""
    
    def __init__(self, name: str, trigger_event: str, handler: Callable):
        self.name = name
        self.trigger_event = trigger_event
        self.handler = handler
        self.enabled = True
    
    async def execute(self, context: CommandContext, event_data: Dict[str, Any]):
        """Execute the hook handler"""
        if self.enabled:
            try:
                return await self.handler(context, event_data)
            except Exception as e:
                logger.error(f"Hook {self.name} failed: {e}")
                return None

class ClaudeIntegration:
    """
    Main Claude Code integration system
    """
    
    def __init__(self):
        self.commands: Dict[str, ClaudeCommand] = {}
        self.hooks: Dict[str, List[ClaudeHook]] = {}
        self.tool_integrations: Dict[ToolIntegration, Any] = {}
        self.context: Optional[CommandContext] = None
        self._initialize_commands()
        self._initialize_hooks()
    
    def _initialize_commands(self):
        """Initialize the core Claude Code commands"""
        
        # TASK ANALYSIS COMMANDS
        self.register_command(ClaudeCommand(
            name="analyze_task",
            category=CommandCategory.TASK_ANALYSIS,
            description="Analyze a software engineering task using the AI-SWE taxonomy",
            usage_pattern="/analyze_task <description> [--scope function|unit|project] [--complexity low|medium|high]",
            parameters={
                "description": {"type": "string", "required": True},
                "scope": {"type": "enum", "values": ["function", "unit", "project"], "default": "auto"},
                "complexity": {"type": "enum", "values": ["low", "medium", "high"], "default": "auto"},
                "intervention": {"type": "enum", "values": ["low", "medium", "high"], "default": "medium"}
            },
            execution_mode=ExecutionMode.INTERACTIVE,
            required_tools=[ToolIntegration.IDE],
            addressed_tasks=["Task Classification", "Challenge Assessment", "Solution Planning"]
        ))
        
        self.register_command(ClaudeCommand(
            name="assess_challenges",
            category=CommandCategory.TASK_ANALYSIS,
            description="Assess potential challenges for the current task",
            usage_pattern="/assess_challenges [--task_name <name>] [--context <file_pattern>]",
            parameters={
                "task_name": {"type": "string", "required": False},
                "context": {"type": "string", "required": False},
                "include_solutions": {"type": "boolean", "default": True}
            },
            execution_mode=ExecutionMode.INTERACTIVE,
            required_tools=[ToolIntegration.STATIC_ANALYSIS],
            addressed_tasks=["Challenge Identification", "Risk Assessment"]
        ))
        
        # CODE GENERATION COMMANDS
        self.register_command(ClaudeCommand(
            name="generate_function",
            category=CommandCategory.CODE_GENERATION,
            description="Generate a function with comprehensive testing and documentation",
            usage_pattern="/generate_function <spec> [--language <lang>] [--style <style>] [--test_coverage <percent>]",
            parameters={
                "spec": {"type": "string", "required": True},
                "language": {"type": "string", "default": "auto"},
                "style": {"type": "string", "default": "project"},
                "test_coverage": {"type": "number", "default": 95},
                "include_docs": {"type": "boolean", "default": True}
            },
            execution_mode=ExecutionMode.SEMI_AUTO,
            required_tools=[ToolIntegration.IDE, ToolIntegration.TESTING],
            addressed_tasks=["Function Completion", "Unit Test Generation", "Code Documentation"]
        ))
        
        self.register_command(ClaudeCommand(
            name="implement_feature",
            category=CommandCategory.CODE_GENERATION,
            description="Implement a complete feature across multiple files",
            usage_pattern="/implement_feature <feature_spec> [--architecture <pattern>] [--integration_tests]",
            parameters={
                "feature_spec": {"type": "string", "required": True},
                "architecture": {"type": "string", "default": "auto"},
                "integration_tests": {"type": "boolean", "default": True},
                "update_docs": {"type": "boolean", "default": True}
            },
            execution_mode=ExecutionMode.INTERACTIVE,
            required_tools=[ToolIntegration.IDE, ToolIntegration.GIT, ToolIntegration.TESTING],
            addressed_tasks=["Natural Language to Code", "Code Documentation", "Testing"]
        ))
        
        # CODE TRANSFORMATION COMMANDS
        self.register_command(ClaudeCommand(
            name="refactor_code",
            category=CommandCategory.CODE_TRANSFORMATION,
            description="Intelligent code refactoring with safety guarantees",
            usage_pattern="/refactor_code <target> [--pattern <refactor_pattern>] [--preserve_tests]",
            parameters={
                "target": {"type": "string", "required": True},
                "pattern": {"type": "enum", "values": ["extract_method", "inline", "move", "rename", "auto"]},
                "preserve_tests": {"type": "boolean", "default": True},
                "backup": {"type": "boolean", "default": True}
            },
            execution_mode=ExecutionMode.SEMI_AUTO,
            required_tools=[ToolIntegration.IDE, ToolIntegration.GIT, ToolIntegration.TESTING],
            addressed_tasks=["Code Refactoring", "Testing", "Version Control"]
        ))
        
        self.register_command(ClaudeCommand(
            name="migrate_api",
            category=CommandCategory.CODE_TRANSFORMATION,
            description="Migrate code to new API versions with compatibility checking",
            usage_pattern="/migrate_api <from_version> <to_version> [--library <name>] [--dry_run]",
            parameters={
                "from_version": {"type": "string", "required": True},
                "to_version": {"type": "string", "required": True},
                "library": {"type": "string", "required": False},
                "dry_run": {"type": "boolean", "default": True},
                "update_tests": {"type": "boolean", "default": True}
            },
            execution_mode=ExecutionMode.INTERACTIVE,
            required_tools=[ToolIntegration.IDE, ToolIntegration.STATIC_ANALYSIS, ToolIntegration.TESTING],
            addressed_tasks=["Code Migration", "Version Management", "Testing"]
        ))
        
        # TESTING AND VERIFICATION COMMANDS
        self.register_command(ClaudeCommand(
            name="generate_tests",
            category=CommandCategory.TESTING_VERIFICATION,
            description="Generate comprehensive test suites with high coverage",
            usage_pattern="/generate_tests <target> [--type unit|integration|e2e] [--coverage <percent>]",
            parameters={
                "target": {"type": "string", "required": True},
                "type": {"type": "enum", "values": ["unit", "integration", "e2e", "all"], "default": "unit"},
                "coverage": {"type": "number", "default": 90},
                "include_edge_cases": {"type": "boolean", "default": True}
            },
            execution_mode=ExecutionMode.SEMI_AUTO,
            required_tools=[ToolIntegration.TESTING, ToolIntegration.IDE],
            addressed_tasks=["Unit Test Generation", "Testing Coverage", "Edge Case Testing"]
        ))
        
        self.register_command(ClaudeCommand(
            name="verify_security",
            category=CommandCategory.TESTING_VERIFICATION,
            description="Comprehensive security vulnerability analysis",
            usage_pattern="/verify_security [--scope <files>] [--include_dependencies]",
            parameters={
                "scope": {"type": "string", "default": "all"},
                "include_dependencies": {"type": "boolean", "default": True},
                "severity_threshold": {"type": "enum", "values": ["low", "medium", "high"], "default": "medium"}
            },
            execution_mode=ExecutionMode.AUTONOMOUS,
            required_tools=[ToolIntegration.STATIC_ANALYSIS],
            addressed_tasks=["Vulnerability Detection", "Security Analysis", "Dependency Scanning"]
        ))
        
        # MAINTENANCE COMMANDS
        self.register_command(ClaudeCommand(
            name="document_code",
            category=CommandCategory.MAINTENANCE,
            description="Generate and update comprehensive code documentation",
            usage_pattern="/document_code [--scope <files>] [--format <format>] [--update_existing]",
            parameters={
                "scope": {"type": "string", "default": "changed"},
                "format": {"type": "enum", "values": ["docstring", "markdown", "rst", "auto"], "default": "auto"},
                "update_existing": {"type": "boolean", "default": True},
                "include_examples": {"type": "boolean", "default": True}
            },
            execution_mode=ExecutionMode.SEMI_AUTO,
            required_tools=[ToolIntegration.DOCUMENTATION, ToolIntegration.IDE],
            addressed_tasks=["Code Documentation", "API Documentation", "Code Examples"]
        ))
        
        self.register_command(ClaudeCommand(
            name="review_pr",
            category=CommandCategory.MAINTENANCE,
            description="Automated pull request review with detailed feedback",
            usage_pattern="/review_pr [--pr_id <id>] [--focus <aspect>]",
            parameters={
                "pr_id": {"type": "string", "required": False},
                "focus": {"type": "enum", "values": ["security", "performance", "style", "all"], "default": "all"},
                "suggest_improvements": {"type": "boolean", "default": True}
            },
            execution_mode=ExecutionMode.SEMI_AUTO,
            required_tools=[ToolIntegration.GIT, ToolIntegration.STATIC_ANALYSIS],
            addressed_tasks=["Pull Request Review", "Code Quality", "Security Review"]
        ))
        
        # SCAFFOLDING COMMANDS
        self.register_command(ClaudeCommand(
            name="setup_project",
            category=CommandCategory.SCAFFOLDING,
            description="Initialize project with best practices and tooling",
            usage_pattern="/setup_project <project_type> [--framework <name>] [--include_ci]",
            parameters={
                "project_type": {"type": "enum", "values": ["web", "api", "cli", "library", "ml"], "required": True},
                "framework": {"type": "string", "required": False},
                "include_ci": {"type": "boolean", "default": True},
                "include_security": {"type": "boolean", "default": True}
            },
            execution_mode=ExecutionMode.INTERACTIVE,
            required_tools=[ToolIntegration.IDE, ToolIntegration.CI_CD],
            addressed_tasks=["Project Setup", "CI/CD Configuration", "Security Setup"]
        ))
        
        self.register_command(ClaudeCommand(
            name="configure_ci",
            category=CommandCategory.SCAFFOLDING,
            description="Setup and optimize CI/CD pipelines",
            usage_pattern="/configure_ci [--platform <platform>] [--include_security] [--optimize]",
            parameters={
                "platform": {"type": "enum", "values": ["github", "gitlab", "jenkins", "auto"], "default": "auto"},
                "include_security": {"type": "boolean", "default": True},
                "optimize": {"type": "boolean", "default": True}
            },
            execution_mode=ExecutionMode.SEMI_AUTO,
            required_tools=[ToolIntegration.CI_CD, ToolIntegration.GIT],
            addressed_tasks=["CI/CD Configuration", "Security Integration", "Pipeline Optimization"]
        ))
        
        # COLLABORATION COMMANDS
        self.register_command(ClaudeCommand(
            name="clarify_requirements",
            category=CommandCategory.COLLABORATION,
            description="Interactive requirements clarification and specification",
            usage_pattern="/clarify_requirements <initial_spec> [--stakeholder <role>]",
            parameters={
                "initial_spec": {"type": "string", "required": True},
                "stakeholder": {"type": "string", "default": "developer"},
                "include_tests": {"type": "boolean", "default": True}
            },
            execution_mode=ExecutionMode.INTERACTIVE,
            required_tools=[ToolIntegration.IDE],
            addressed_tasks=["Requirements Analysis", "Specification Clarification", "Stakeholder Communication"]
        ))
        
        self.register_command(ClaudeCommand(
            name="explain_code",
            category=CommandCategory.COLLABORATION,
            description="Generate detailed code explanations and walkthroughs",
            usage_pattern="/explain_code <target> [--audience <level>] [--format <format>]",
            parameters={
                "target": {"type": "string", "required": True},
                "audience": {"type": "enum", "values": ["beginner", "intermediate", "expert"], "default": "intermediate"},
                "format": {"type": "enum", "values": ["text", "diagram", "video"], "default": "text"}
            },
            execution_mode=ExecutionMode.AUTONOMOUS,
            required_tools=[ToolIntegration.DOCUMENTATION],
            addressed_tasks=["Code Understanding", "Knowledge Transfer", "Documentation"]
        ))
        
        # EVALUATION COMMANDS
        self.register_command(ClaudeCommand(
            name="benchmark_performance",
            category=CommandCategory.EVALUATION,
            description="Comprehensive performance benchmarking and optimization suggestions",
            usage_pattern="/benchmark_performance [--target <scope>] [--metrics <metrics>]",
            parameters={
                "target": {"type": "string", "default": "all"},
                "metrics": {"type": "list", "default": ["time", "memory", "throughput"]},
                "compare_baseline": {"type": "boolean", "default": True}
            },
            execution_mode=ExecutionMode.AUTONOMOUS,
            required_tools=[ToolIntegration.STATIC_ANALYSIS, ToolIntegration.TESTING],
            addressed_tasks=["Performance Analysis", "Optimization", "Benchmarking"]
        ))
        
        logger.info(f"Initialized {len(self.commands)} Claude Code commands")
    
    def _initialize_hooks(self):
        """Initialize event hooks for Claude integration"""
        
        # File change hooks
        self.register_hook(ClaudeHook(
            name="auto_test_on_change",
            trigger_event="file_saved",
            handler=self._auto_run_tests
        ))
        
        self.register_hook(ClaudeHook(
            name="auto_format_on_save",
            trigger_event="file_saved", 
            handler=self._auto_format_code
        ))
        
        # Git hooks
        self.register_hook(ClaudeHook(
            name="pre_commit_check",
            trigger_event="pre_commit",
            handler=self._pre_commit_validation
        ))
        
        self.register_hook(ClaudeHook(
            name="post_merge_update",
            trigger_event="post_merge",
            handler=self._post_merge_actions
        ))
        
        # AI workflow hooks
        self.register_hook(ClaudeHook(
            name="challenge_detection",
            trigger_event="task_start",
            handler=self._detect_challenges
        ))
        
        self.register_hook(ClaudeHook(
            name="solution_suggestion",
            trigger_event="challenge_detected",
            handler=self._suggest_solutions
        ))
        
        logger.info(f"Initialized {sum(len(hooks) for hooks in self.hooks.values())} Claude hooks")
    
    def register_command(self, command: ClaudeCommand):
        """Register a new Claude command"""
        self.commands[command.name] = command
        logger.debug(f"Registered command: /{command.name}")
    
    def register_hook(self, hook: ClaudeHook):
        """Register an event hook"""
        if hook.trigger_event not in self.hooks:
            self.hooks[hook.trigger_event] = []
        self.hooks[hook.trigger_event].append(hook)
        logger.debug(f"Registered hook: {hook.name} for {hook.trigger_event}")
    
    async def execute_command(self, command_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a Claude command"""
        if command_name not in self.commands:
            return {"error": f"Unknown command: {command_name}"}
        
        command = self.commands[command_name]
        
        # Validate parameters
        validation_result = self._validate_parameters(command, parameters)
        if validation_result["valid"] == False:
            return {"error": f"Parameter validation failed: {validation_result['errors']}"}
        
        # Check execution mode and get user confirmation if needed
        if command.execution_mode == ExecutionMode.INTERACTIVE:
            confirmation = await self._get_user_confirmation(command, parameters)
            if not confirmation:
                return {"cancelled": True}
        
        # Execute the command
        try:
            if command.implementation:
                result = await command.implementation(self.context, parameters)
            else:
                result = await self._default_command_handler(command, parameters)
            
            # Trigger post-execution hooks
            await self._trigger_hooks("command_executed", {
                "command": command_name,
                "parameters": parameters,
                "result": result
            })
            
            return result
        
        except Exception as e:
            logger.error(f"Command {command_name} failed: {e}")
            return {"error": str(e)}
    
    async def _trigger_hooks(self, event: str, data: Dict[str, Any]):
        """Trigger all hooks for a specific event"""
        if event in self.hooks:
            for hook in self.hooks[event]:
                await hook.execute(self.context, data)
    
    def _validate_parameters(self, command: ClaudeCommand, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate command parameters"""
        errors = []
        
        for param_name, param_config in command.parameters.items():
            if param_config.get("required", False) and param_name not in parameters:
                errors.append(f"Missing required parameter: {param_name}")
            
            if param_name in parameters:
                value = parameters[param_name]
                param_type = param_config.get("type")
                
                if param_type == "enum" and value not in param_config.get("values", []):
                    errors.append(f"Invalid value for {param_name}: {value}")
        
        return {"valid": len(errors) == 0, "errors": errors}
    
    async def _get_user_confirmation(self, command: ClaudeCommand, parameters: Dict[str, Any]) -> bool:
        """Get user confirmation for interactive commands"""
        # This would integrate with the actual UI/CLI
        logger.info(f"Requesting confirmation for command: {command.name}")
        return True  # Placeholder
    
    async def _default_command_handler(self, command: ClaudeCommand, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Default handler for commands without custom implementation"""
        return {
            "command": command.name,
            "status": "executed",
            "message": f"Executed {command.name} with parameters: {parameters}"
        }
    
    # Hook implementations
    async def _auto_run_tests(self, context: CommandContext, event_data: Dict[str, Any]):
        """Auto-run tests when files are saved"""
        # Implementation would trigger test runs
        pass
    
    async def _auto_format_code(self, context: CommandContext, event_data: Dict[str, Any]):
        """Auto-format code on save"""
        # Implementation would run code formatters
        pass
    
    async def _pre_commit_validation(self, context: CommandContext, event_data: Dict[str, Any]):
        """Pre-commit validation checks"""
        # Implementation would run linting, testing, security checks
        pass
    
    async def _post_merge_actions(self, context: CommandContext, event_data: Dict[str, Any]):
        """Actions to take after git merge"""
        # Implementation would update dependencies, run tests, etc.
        pass
    
    async def _detect_challenges(self, context: CommandContext, event_data: Dict[str, Any]):
        """Detect potential challenges for the current task"""
        # Implementation would analyze task and identify challenges
        pass
    
    async def _suggest_solutions(self, context: CommandContext, event_data: Dict[str, Any]):
        """Suggest solutions for detected challenges"""
        # Implementation would recommend solution approaches
        pass
    
    def get_available_commands(self, category: Optional[CommandCategory] = None) -> List[ClaudeCommand]:
        """Get list of available commands, optionally filtered by category"""
        commands = list(self.commands.values())
        if category:
            commands = [cmd for cmd in commands if cmd.category == category]
        return commands
    
    def get_command_help(self, command_name: str) -> Optional[str]:
        """Get help text for a specific command"""
        if command_name in self.commands:
            cmd = self.commands[command_name]
            help_text = f"""
Command: /{cmd.name}
Category: {cmd.category.value}
Description: {cmd.description}
Usage: {cmd.usage_pattern}
Execution Mode: {cmd.execution_mode.value}
Required Tools: {[tool.value for tool in cmd.required_tools]}
Addressed Tasks: {cmd.addressed_tasks}
"""
            return help_text
        return None

# Global Claude integration instance
claude_integration = ClaudeIntegration()

__all__ = [
    'CommandCategory', 'ExecutionMode', 'ToolIntegration',
    'CommandContext', 'ClaudeCommand', 'ClaudeHook', 'ClaudeIntegration',
    'claude_integration'
] 