"""
AI for Software Engineering Framework

This module implements the comprehensive taxonomy and measurement system
described in "Challenges and Paths Towards AI for Software Engineering".
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScopeMeasure(Enum):
    """
    Scope Measure: The extent of changes that the AI makes to the codebase
    """
    FUNCTION_LEVEL = "function"  # Single, self-contained functions (HumanEval, MBPP)
    UNIT_LEVEL = "unit"          # Larger chunks, files, classes (FullStackBench, BigCodeBench) 
    PROJECT_LEVEL = "project"    # Entire repositories (SWE-Bench, Commit0)

class LogicalComplexity(Enum):
    """
    Logical Complexity: Reasoning abilities required to devise algorithms
    """
    LOW = "low"       # Little to no reasoning (CRUD, basic API usage)
    MEDIUM = "medium" # Standard algorithmic reasoning (LeetCode, multithreading)
    HIGH = "high"     # Complex algorithms, cryptography, competition programming

class HumanIntervention(Enum):
    """
    Human Intervention Level: Degree of autonomy in AI-human collaboration
    """
    LOW = "low"       # Human-controlled with AI as tool
    MEDIUM = "medium" # Collaborative human-AI coordination
    HIGH = "high"     # AI-driven with human oversight

class TaskCategory(Enum):
    """
    Main categories of AI Software Engineering tasks
    """
    CODE_GENERATION = "code_generation"
    CODE_TRANSFORMATION = "code_transformation" 
    TESTING_ANALYSIS = "testing_analysis"
    SOFTWARE_MAINTENANCE = "software_maintenance"
    SCAFFOLDING_METACODE = "scaffolding_metacode"
    FORMAL_VERIFICATION = "formal_verification"

@dataclass
class TaskMetrics:
    """
    Three-dimensional measurement of AI-SWE tasks
    """
    scope: ScopeMeasure
    complexity: LogicalComplexity
    intervention: HumanIntervention
    
    def __str__(self) -> str:
        return f"Scope: {self.scope.value}, Complexity: {self.complexity.value}, Intervention: {self.intervention.value}"

@dataclass
class AITask:
    """
    Represents a specific AI Software Engineering task
    """
    name: str
    category: TaskCategory
    metrics: TaskMetrics
    description: str
    examples: List[str]
    challenges: List[str]
    benchmarks: List[str]
    
    def __str__(self) -> str:
        return f"{self.name} ({self.category.value}): {self.metrics}"

class FrameworkRegistry:
    """
    Central registry for AI-SWE tasks, challenges, and solutions
    """
    
    def __init__(self):
        self.tasks: Dict[str, AITask] = {}
        self.challenges: Dict[str, Any] = {}
        self.solutions: Dict[str, Any] = {}
        self._initialize_core_tasks()
    
    def _initialize_core_tasks(self):
        """Initialize the core task taxonomy from the research paper"""
        
        # Code Generation Tasks
        self.register_task(AITask(
            name="Function Completion",
            category=TaskCategory.CODE_GENERATION,
            metrics=TaskMetrics(ScopeMeasure.FUNCTION_LEVEL, LogicalComplexity.LOW, HumanIntervention.LOW),
            description="Complete code snippets at function level with tab completion",
            examples=["GitHub Copilot tab completion", "Function signature completion"],
            challenges=["Context understanding", "Code quality"],
            benchmarks=["HumanEval", "MBPP"]
        ))
        
        self.register_task(AITask(
            name="Natural Language to Code",
            category=TaskCategory.CODE_GENERATION,
            metrics=TaskMetrics(ScopeMeasure.UNIT_LEVEL, LogicalComplexity.MEDIUM, HumanIntervention.MEDIUM),
            description="Generate code from natural language specifications",
            examples=["Cursor Composer", "Detailed function implementation"],
            challenges=["Specification ambiguity", "Complex requirements"],
            benchmarks=["APPS", "CodeContests", "LiveCodeBench"]
        ))
        
        # Code Transformation Tasks  
        self.register_task(AITask(
            name="Code Refactoring",
            category=TaskCategory.CODE_TRANSFORMATION,
            metrics=TaskMetrics(ScopeMeasure.PROJECT_LEVEL, LogicalComplexity.LOW, HumanIntervention.HIGH),
            description="Restructure code while maintaining functionality",
            examples=["React Fiber architecture refactor", "Extract helper methods"],
            challenges=["Maintainability trade-offs", "Scope propagation"],
            benchmarks=["RefactorBench"]
        ))
        
        self.register_task(AITask(
            name="Code Migration",
            category=TaskCategory.CODE_TRANSFORMATION,
            metrics=TaskMetrics(ScopeMeasure.PROJECT_LEVEL, LogicalComplexity.HIGH, HumanIntervention.HIGH),
            description="Migrate code between languages or versions",
            examples=["C to Rust translation", "Python 2 to 3 migration"],
            challenges=["Semantic preservation", "Cross-system dependencies"],
            benchmarks=["Syzygy", "C2SaferRust"]
        ))
        
        # Testing and Analysis Tasks
        self.register_task(AITask(
            name="Unit Test Generation", 
            category=TaskCategory.TESTING_ANALYSIS,
            metrics=TaskMetrics(ScopeMeasure.FUNCTION_LEVEL, LogicalComplexity.MEDIUM, HumanIntervention.LOW),
            description="Generate comprehensive unit tests for code coverage",
            examples=["Meta's ACH system", "Property-based testing"],
            challenges=["Edge case coverage", "Test quality"],
            benchmarks=["TestGenEval", "CodeT"]
        ))
        
        self.register_task(AITask(
            name="Vulnerability Detection",
            category=TaskCategory.TESTING_ANALYSIS,
            metrics=TaskMetrics(ScopeMeasure.PROJECT_LEVEL, LogicalComplexity.HIGH, HumanIntervention.MEDIUM),
            description="Identify security vulnerabilities and zero-day exploits",
            examples=["BigSleep SQLite vulnerability", "Project Zero variant analysis"],
            challenges=["Complex attack vectors", "False positives"],
            benchmarks=["SecurityEval", "CyberSecEval"]
        ))
        
        # Software Maintenance Tasks
        self.register_task(AITask(
            name="Code Documentation",
            category=TaskCategory.SOFTWARE_MAINTENANCE,
            metrics=TaskMetrics(ScopeMeasure.UNIT_LEVEL, LogicalComplexity.LOW, HumanIntervention.LOW),
            description="Generate and maintain code documentation",
            examples=["Function docstrings", "API documentation"],
            challenges=["Synchronization with code", "Quality assessment"],
            benchmarks=["CodeXGLUE", "RepoAgent"]
        ))
        
        self.register_task(AITask(
            name="Code Navigation",
            category=TaskCategory.SOFTWARE_MAINTENANCE,
            metrics=TaskMetrics(ScopeMeasure.PROJECT_LEVEL, LogicalComplexity.MEDIUM, HumanIntervention.MEDIUM),
            description="Find relevant functionality in large codebases",
            examples=["Feature location", "Bug root cause analysis"],
            challenges=["Semantic understanding", "Call stack complexity"],
            benchmarks=["CodeRAGBench", "BRIGHT"]
        ))
        
        # Scaffolding and Meta-Code Tasks
        self.register_task(AITask(
            name="CI/CD Configuration",
            category=TaskCategory.SCAFFOLDING_METACODE,
            metrics=TaskMetrics(ScopeMeasure.PROJECT_LEVEL, LogicalComplexity.MEDIUM, HumanIntervention.HIGH),
            description="Generate and manage CI/CD pipelines and infrastructure",
            examples=["GitHub Actions", "Terraform generation"],
            challenges=["Security configurations", "Complex dependencies"],
            benchmarks=["Ciri", "Terrateam"]
        ))
        
        # Formal Verification Tasks
        self.register_task(AITask(
            name="Property Verification",
            category=TaskCategory.FORMAL_VERIFICATION,
            metrics=TaskMetrics(ScopeMeasure.UNIT_LEVEL, LogicalComplexity.HIGH, HumanIntervention.HIGH),
            description="Prove specific properties of code correctness",
            examples=["Memory safety proofs", "Concurrency verification"],
            challenges=["False positives", "Specification completeness"],
            benchmarks=["DafnyBench", "miniCodeProps"]
        ))
        
        logger.info(f"Initialized framework with {len(self.tasks)} core tasks")
    
    def register_task(self, task: AITask):
        """Register a new AI-SWE task in the framework"""
        self.tasks[task.name] = task
        logger.debug(f"Registered task: {task.name}")
    
    def get_tasks_by_category(self, category: TaskCategory) -> List[AITask]:
        """Get all tasks in a specific category"""
        return [task for task in self.tasks.values() if task.category == category]
    
    def get_tasks_by_metrics(self, scope: Optional[ScopeMeasure] = None, 
                           complexity: Optional[LogicalComplexity] = None,
                           intervention: Optional[HumanIntervention] = None) -> List[AITask]:
        """Filter tasks by measurement dimensions"""
        filtered_tasks = []
        for task in self.tasks.values():
            if scope and task.metrics.scope != scope:
                continue
            if complexity and task.metrics.complexity != complexity:
                continue  
            if intervention and task.metrics.intervention != intervention:
                continue
            filtered_tasks.append(task)
        return filtered_tasks
    
    def get_task_distribution(self) -> Dict[str, Dict[str, int]]:
        """Get statistical distribution of tasks across dimensions"""
        distribution = {
            "scope": {scope.value: 0 for scope in ScopeMeasure},
            "complexity": {complexity.value: 0 for complexity in LogicalComplexity},
            "intervention": {intervention.value: 0 for intervention in HumanIntervention},
            "category": {category.value: 0 for category in TaskCategory}
        }
        
        for task in self.tasks.values():
            distribution["scope"][task.metrics.scope.value] += 1
            distribution["complexity"][task.metrics.complexity.value] += 1
            distribution["intervention"][task.metrics.intervention.value] += 1
            distribution["category"][task.category.value] += 1
            
        return distribution

# Global framework instance
framework = FrameworkRegistry()

__all__ = [
    'ScopeMeasure', 'LogicalComplexity', 'HumanIntervention', 'TaskCategory',
    'TaskMetrics', 'AITask', 'FrameworkRegistry', 'framework'
] 