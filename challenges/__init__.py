"""
AI-SWE Challenge Assessment System

Implements systematic evaluation of the 9 key challenges identified in
"Challenges and Paths Towards AI for Software Engineering".
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
import logging

logger = logging.getLogger(__name__)

class ChallengeCategory(Enum):
    """
    Nine key challenges that limit current AI-SWE approaches
    """
    EVALUATION_BENCHMARKS = "evaluation_benchmarks"
    EFFECTIVE_TOOL_USAGE = "effective_tool_usage" 
    HUMAN_AI_COLLABORATION = "human_ai_collaboration"
    LONG_HORIZON_PLANNING = "long_horizon_planning"
    LARGE_SCOPE_CONTEXTS = "large_scope_contexts"
    SEMANTIC_UNDERSTANDING = "semantic_understanding"
    LOW_RESOURCE_ADAPTATION = "low_resource_adaptation"
    VERSION_MANAGEMENT = "version_management"
    HIGH_COMPLEXITY_OOD = "high_complexity_ood"

class SeverityLevel(Enum):
    """
    Impact severity of challenges on AI-SWE systems
    """
    CRITICAL = "critical"     # Prevents successful completion
    HIGH = "high"            # Significantly degrades performance
    MEDIUM = "medium"        # Noticeable performance impact
    LOW = "low"              # Minor impact on edge cases

@dataclass
class ChallengeMetrics:
    """
    Quantitative assessment of challenge impact
    """
    severity: SeverityLevel
    frequency: float          # How often the challenge occurs (0-1)
    task_coverage: float      # Fraction of tasks affected (0-1)
    solution_readiness: float # How close we are to solving it (0-1)
    
    def impact_score(self) -> float:
        """Calculate overall impact score"""
        severity_weights = {
            SeverityLevel.CRITICAL: 1.0,
            SeverityLevel.HIGH: 0.8,
            SeverityLevel.MEDIUM: 0.6,
            SeverityLevel.LOW: 0.4
        }
        return (severity_weights[self.severity] * 
                self.frequency * 
                self.task_coverage * 
                (1 - self.solution_readiness))

@dataclass
class Challenge:
    """
    Represents a specific challenge in AI-SWE systems
    """
    name: str
    category: ChallengeCategory
    description: str
    symptoms: List[str]
    affected_tasks: Set[str]
    root_causes: List[str]
    examples: List[str]
    metrics: ChallengeMetrics
    related_challenges: List[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        return f"{self.name} ({self.category.value}): Impact {self.metrics.impact_score():.2f}"

class ChallengeRegistry:
    """
    Comprehensive registry of AI-SWE challenges and their assessments
    """
    
    def __init__(self):
        self.challenges: Dict[str, Challenge] = {}
        self._initialize_core_challenges()
    
    def _initialize_core_challenges(self):
        """Initialize the 9 core challenges from the research paper"""
        
        # Challenge 1: Evaluation and Benchmarks
        self.register_challenge(Challenge(
            name="Evaluation and Benchmarks",
            category=ChallengeCategory.EVALUATION_BENCHMARKS,
            description="Today's code LLM evaluations focus on narrow tasks, suffer from contamination, and don't reliably measure real-world software engineering abilities",
            symptoms=[
                "Performance on benchmarks doesn't match user experience",
                "Contamination degrades benchmark validity over time",
                "Limited task diversity in evaluations",
                "Lack of human-AI interaction assessment"
            ],
            affected_tasks={
                "Function Completion", "Natural Language to Code", "Code Refactoring",
                "Unit Test Generation", "Code Documentation", "Property Verification"
            },
            root_causes=[
                "Narrow focus on code generation tasks",
                "Public benchmark exposure leads to contamination",
                "Difficulty quantifying software engineering qualities",
                "Lack of construct validity for real-world scenarios"
            ],
            examples=[
                "HumanEval performance vs actual coding assistance quality",
                "SWE-Bench contamination over time",
                "Missing evaluation for code maintainability"
            ],
            metrics=ChallengeMetrics(
                severity=SeverityLevel.CRITICAL,
                frequency=0.9,
                task_coverage=0.8,
                solution_readiness=0.3
            )
        ))
        
        # Challenge 2: Effective Tool Usage  
        self.register_challenge(Challenge(
            name="Effective Tool Usage",
            category=ChallengeCategory.EFFECTIVE_TOOL_USAGE,
            description="AI needs to select, use, and interpret outputs from programming tools dynamically",
            symptoms=[
                "Models don't proactively use appropriate tools",
                "Incorrect tool invocation parameters",
                "Failure to interpret tool outputs correctly",
                "Limited integration with development workflows"
            ],
            affected_tasks={
                "Code Migration", "Vulnerability Detection", "Code Navigation",
                "CI/CD Configuration", "Property Verification"
            },
            root_causes=[
                "Lack of training on tool interaction",
                "Complex tool APIs and documentation",
                "Dynamic tool selection requirements",
                "Insufficient feedback integration"
            ],
            examples=[
                "CSI performance profiler integration complexity",
                "Debugger step-through navigation challenges",
                "Static analysis tool output interpretation"
            ],
            metrics=ChallengeMetrics(
                severity=SeverityLevel.HIGH,
                frequency=0.7,
                task_coverage=0.6,
                solution_readiness=0.4
            )
        ))
        
        # Challenge 3: Human-AI Collaboration
        self.register_challenge(Challenge(
            name="Human-AI Collaboration",
            category=ChallengeCategory.HUMAN_AI_COLLABORATION,
            description="Vague specifications, lack of controllability, and limited collaboration interfaces",
            symptoms=[
                "Generated code doesn't match user intent",
                "No reliable way to steer model behavior",
                "Models rarely ask clarifying questions",
                "Poor transparency in agent actions"
            ],
            affected_tasks={
                "Natural Language to Code", "Code Refactoring", "Code Migration",
                "Code Navigation", "CI/CD Configuration"
            },
            root_causes=[
                "Ambiguous natural language specifications",
                "Lack of uncertainty quantification",
                "Implicit constraints and trade-offs",
                "Limited multi-turn interaction training"
            ],
            examples=[
                "Astropy issue missing serializer-deserializer pattern",
                "Academic website requirements ambiguity",
                "Missing style guide adherence"
            ],
            metrics=ChallengeMetrics(
                severity=SeverityLevel.CRITICAL,
                frequency=0.8,
                task_coverage=0.9,
                solution_readiness=0.2
            )
        ))
        
        # Challenge 4: Long-Horizon Code Planning
        self.register_challenge(Challenge(
            name="Long-Horizon Code Planning",
            category=ChallengeCategory.LONG_HORIZON_PLANNING,
            description="Designing good abstractions and respecting modularity in large software projects",
            symptoms=[
                "Poor abstraction choices affect extensibility",
                "Code duplication instead of reuse",
                "Suboptimal data structure selection",
                "Quality degradation with RL optimization"
            ],
            affected_tasks={
                "Code Refactoring", "Code Migration", "Natural Language to Code",
                "CI/CD Configuration"
            },
            root_causes=[
                "Training optimized for correctness over quality",
                "Lack of long-term consequence modeling",
                "Insufficient exposure to design patterns",
                "Missing domain expertise integration"
            ],
            examples=[
                "Database schema design trade-offs",
                "Library API design for extensibility",
                "React component architecture decisions"
            ],
            metrics=ChallengeMetrics(
                severity=SeverityLevel.HIGH,
                frequency=0.6,
                task_coverage=0.5,
                solution_readiness=0.3
            )
        ))
        
        # Challenge 5: Large Scope and Long Contexts
        self.register_challenge(Challenge(
            name="Large Scope and Long Contexts",
            category=ChallengeCategory.LARGE_SCOPE_CONTEXTS,
            description="Repository-level tasks require context beyond current model limits, with retrieval challenges",
            symptoms=[
                "Context length limitations for large codebases",
                "Retrieval returns syntactically similar but semantically irrelevant code",
                "Poor code reuse and adaptation",
                "Failure to maintain consistency across files"
            ],
            affected_tasks={
                "Code Migration", "Code Refactoring", "Code Navigation",
                "Vulnerability Detection", "CI/CD Configuration"
            },
            root_causes=[
                "Millions of lines exceed context windows",
                "Embeddings capture syntax over semantics",
                "Complex code reuse requirements",
                "Insufficient global codebase understanding"
            ],
            examples=[
                "Google's billion-line repositories",
                "Chart.js BM25 retrieval failures",
                "Datadog log analysis complexity"
            ],
            metrics=ChallengeMetrics(
                severity=SeverityLevel.HIGH,
                frequency=0.8,
                task_coverage=0.7,
                solution_readiness=0.4
            )
        ))
        
        # Challenge 6: Semantic Understanding
        self.register_challenge(Challenge(
            name="Semantic Understanding of Codebases", 
            category=ChallengeCategory.SEMANTIC_UNDERSTANDING,
            description="Lack of holistic understanding of code structure, algorithms, and program invariants",
            symptoms=[
                "Inability to understand complex code relationships",
                "Missing awareness of program invariants",
                "Poor generalization across coding tasks",
                "Failure to identify bottlenecks correctly"
            ],
            affected_tasks={
                "Code Migration", "Vulnerability Detection", "Code Navigation",
                "Code Refactoring", "Property Verification"
            },
            root_causes=[
                "Training focus on generation over understanding",
                "Complex algorithmic relationships",
                "Custom algorithms outside training data",
                "Lack of execution-aware training"
            ],
            examples=[
                "Query optimization requiring algorithm understanding",
                "Complex nested function interactions",
                "Performance bottleneck identification"
            ],
            metrics=ChallengeMetrics(
                severity=SeverityLevel.CRITICAL,
                frequency=0.7,
                task_coverage=0.8,
                solution_readiness=0.2
            )
        ))
        
        # Challenge 7: Low-Resource Languages and Specialized Libraries
        self.register_challenge(Challenge(
            name="Low-Resource Languages and Specialized Libraries",
            category=ChallengeCategory.LOW_RESOURCE_ADAPTATION,
            description="Poor performance in domain-specific languages and custom/proprietary libraries",
            symptoms=[
                "Syntactic errors in low-resource languages",
                "Hallucinated functions from similar languages",
                "Incorrect library usage patterns",
                "Poor semantic understanding of constructs"
            ],
            affected_tasks={
                "Natural Language to Code", "Code Migration", "Code Documentation",
                "Unit Test Generation", "Property Verification"
            },
            root_causes=[
                "Limited training data for specialized domains",
                "Overfitting to high-resource languages",
                "Proprietary codebase distribution shift",
                "Complex domain-specific semantics"
            ],
            examples=[
                "Triton GPU programming syntax errors",
                "Lean theorem proving hallucinations",
                "Hazel language construct borrowing"
            ],
            metrics=ChallengeMetrics(
                severity=SeverityLevel.HIGH,
                frequency=0.5,
                task_coverage=0.4,
                solution_readiness=0.3
            )
        ))
        
        # Challenge 8: Library and API Version Updates
        self.register_challenge(Challenge(
            name="Library and API Version Updates",
            category=ChallengeCategory.VERSION_MANAGEMENT,
            description="Difficulty adapting to rapidly changing libraries and maintaining version consistency",
            symptoms=[
                "Using deprecated API patterns",
                "Mixing constructs from different versions",
                "Inability to identify correct versions",
                "Resistance to new paradigms and features"
            ],
            affected_tasks={
                "Natural Language to Code", "Code Migration", "Code Documentation",
                "Unit Test Generation", "CI/CD Configuration"
            },
            root_causes=[
                "Continuous library evolution",
                "Training data lag behind current versions",
                "Complex version dependency inference",
                "Paradigm shift integration challenges"
            ],
            examples=[
                "React Hooks vs class components",
                "Python typing module evolution",
                "Next.js App Router navigation changes",
                "Lean 3 to Lean 4 syntax migration"
            ],
            metrics=ChallengeMetrics(
                severity=SeverityLevel.MEDIUM,
                frequency=0.6,
                task_coverage=0.6,
                solution_readiness=0.3
            )
        ))
        
        # Challenge 9: High Logical Complexity and OOD Domains  
        self.register_challenge(Challenge(
            name="High Logical Complexity and OOD Domains",
            category=ChallengeCategory.HIGH_COMPLEXITY_OOD,
            description="Difficulty with research-level problems requiring novel algorithms and complex reasoning",
            symptoms=[
                "Failure on challenging algorithmic problems",
                "Poor performance in specialized domains",
                "Inability to discover novel optimizations",
                "Limited progress without extensive feedback"
            ],
            affected_tasks={
                "Code Migration", "Vulnerability Detection", "Property Verification",
                "Natural Language to Code"
            },
            root_causes=[
                "Rare occurrence in training data",
                "Complex domain-specific knowledge requirements",
                "Large search spaces without clear feedback",
                "Novel algorithm discovery challenges"
            ],
            examples=[
                "AlphaDev sorting kernel optimization",
                "FSCQ file system verification",
                "Cryptographic vulnerability discovery",
                "GPU kernel superoptimization"
            ],
            metrics=ChallengeMetrics(
                severity=SeverityLevel.CRITICAL,
                frequency=0.3,
                task_coverage=0.3,
                solution_readiness=0.1
            )
        ))
        
        # Set up challenge relationships
        self._initialize_challenge_relationships()
        
        logger.info(f"Initialized challenge registry with {len(self.challenges)} challenges")
    
    def _initialize_challenge_relationships(self):
        """Set up relationships between related challenges"""
        relationships = {
            "Evaluation and Benchmarks": ["Human-AI Collaboration", "Semantic Understanding"],
            "Effective Tool Usage": ["Large Scope and Long Contexts", "High Logical Complexity and OOD"],
            "Human-AI Collaboration": ["Long-Horizon Code Planning", "Evaluation and Benchmarks"],
            "Long-Horizon Code Planning": ["Semantic Understanding", "Human-AI Collaboration"], 
            "Large Scope and Long Contexts": ["Semantic Understanding", "Effective Tool Usage"],
            "Semantic Understanding": ["Large Scope and Long Contexts", "Low-Resource Languages and Specialized Libraries"],
            "Low-Resource Languages and Specialized Libraries": ["Version Management", "Semantic Understanding"],
            "Library and API Version Updates": ["Low-Resource Languages and Specialized Libraries", "Human-AI Collaboration"],
            "High Logical Complexity and OOD Domains": ["Effective Tool Usage", "Long-Horizon Code Planning"]
        }
        
        for challenge_name, related_names in relationships.items():
            if challenge_name in self.challenges:
                self.challenges[challenge_name].related_challenges = related_names
    
    def register_challenge(self, challenge: Challenge):
        """Register a new challenge in the system"""
        self.challenges[challenge.name] = challenge
        logger.debug(f"Registered challenge: {challenge.name}")
    
    def get_challenges_by_category(self, category: ChallengeCategory) -> List[Challenge]:
        """Get all challenges in a specific category"""
        return [c for c in self.challenges.values() if c.category == category]
    
    def get_challenges_by_severity(self, severity: SeverityLevel) -> List[Challenge]:
        """Get challenges by severity level"""
        return [c for c in self.challenges.values() if c.metrics.severity == severity]
    
    def get_challenge_impact_ranking(self) -> List[Challenge]:
        """Get challenges ranked by impact score"""
        return sorted(self.challenges.values(), 
                     key=lambda c: c.metrics.impact_score(), 
                     reverse=True)
    
    def get_task_challenges(self, task_name: str) -> List[Challenge]:
        """Get all challenges that affect a specific task"""
        return [c for c in self.challenges.values() if task_name in c.affected_tasks]
    
    def assess_system_readiness(self) -> Dict[str, float]:
        """Assess overall system readiness across challenge dimensions"""
        categories = {}
        for challenge in self.challenges.values():
            cat = challenge.category.value
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(challenge.metrics.solution_readiness)
        
        return {cat: sum(scores) / len(scores) for cat, scores in categories.items()}
    
    def get_priority_challenges(self, top_n: int = 5) -> List[Challenge]:
        """Get the highest priority challenges to address"""
        return self.get_challenge_impact_ranking()[:top_n]

# Global challenge registry
challenge_registry = ChallengeRegistry()

__all__ = [
    'ChallengeCategory', 'SeverityLevel', 'ChallengeMetrics', 'Challenge',
    'ChallengeRegistry', 'challenge_registry'
] 