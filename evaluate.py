#!/usr/bin/env python3
"""
AI for Software Engineering Framework - Evaluation CLI

Comprehensive command-line interface for evaluating AI-SWE tasks,
assessing challenges, exploring solutions, and using Claude Code integration.
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import asdict
import logging

# Import framework components
from framework import (
    framework, ScopeMeasure, LogicalComplexity, HumanIntervention, 
    TaskCategory, AITask, TaskMetrics
)
from challenges import (
    challenge_registry, ChallengeCategory, SeverityLevel, Challenge
)
from solutions import (
    solution_registry, SolutionCategory, ImplementationStatus, 
    EffectivenessLevel, Solution
)
from claude import (
    claude_integration, CommandCategory, ExecutionMode, ClaudeCommand
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FrameworkEvaluator:
    """
    Main evaluation engine for the AI-SWE framework
    """
    
    def __init__(self):
        self.framework = framework
        self.challenges = challenge_registry
        self.solutions = solution_registry
        self.claude = claude_integration
    
    def evaluate_task(self, task_name: str) -> Dict[str, Any]:
        """Evaluate a specific AI-SWE task"""
        if task_name not in self.framework.tasks:
            return {"error": f"Task '{task_name}' not found"}
        
        task = self.framework.tasks[task_name]
        
        # Get challenges affecting this task
        task_challenges = self.challenges.get_task_challenges(task_name)
        
        # Get solutions addressing challenges for this task
        task_solutions = []
        for challenge in task_challenges:
            solutions = self.solutions.get_solutions_for_challenge(challenge.name)
            task_solutions.extend(solutions)
        
        # Remove duplicates
        task_solutions = list(set(task_solutions))
        
        # Calculate readiness score
        if task_challenges:
            avg_solution_readiness = sum(c.metrics.solution_readiness for c in task_challenges) / len(task_challenges)
            challenge_impact = sum(c.metrics.impact_score() for c in task_challenges) / len(task_challenges)
        else:
            avg_solution_readiness = 1.0
            challenge_impact = 0.0
        
        readiness_score = max(0, avg_solution_readiness - challenge_impact)
        
        return {
            "task": asdict(task),
            "challenges": [asdict(c) for c in task_challenges],
            "solutions": [asdict(s) for s in task_solutions],
            "readiness_score": readiness_score,
            "recommendation": self._get_task_recommendation(task, task_challenges, task_solutions, readiness_score)
        }
    
    def _get_task_recommendation(self, task: AITask, challenges: List[Challenge], 
                               solutions: List[Solution], readiness_score: float) -> str:
        """Generate recommendation for task implementation"""
        if readiness_score > 0.8:
            return "HIGH CONFIDENCE: Task is well-understood with mature solutions available"
        elif readiness_score > 0.6:
            return "MEDIUM CONFIDENCE: Task has some challenges but viable solutions exist"
        elif readiness_score > 0.4:
            return "LOW CONFIDENCE: Significant challenges present, solutions in development"
        else:
            return "RESEARCH NEEDED: Major challenges without mature solutions"
    
    def analyze_challenge_coverage(self) -> Dict[str, Any]:
        """Analyze how well solutions cover different challenges"""
        coverage = self.solutions.assess_solution_coverage()
        
        # Calculate overall coverage statistics
        total_challenges = len(self.challenges.challenges)
        covered_challenges = sum(1 for count in coverage.values() if count > 0)
        avg_solutions_per_challenge = sum(coverage.values()) / total_challenges if total_challenges > 0 else 0
        
        # Identify gaps
        uncovered_challenges = [name for name, count in coverage.items() if count == 0]
        under_addressed = [name for name, count in coverage.items() if 0 < count < 2]
        
        return {
            "total_challenges": total_challenges,
            "covered_challenges": covered_challenges,
            "coverage_percentage": (covered_challenges / total_challenges) * 100 if total_challenges > 0 else 0,
            "avg_solutions_per_challenge": avg_solutions_per_challenge,
            "coverage_details": coverage,
            "gaps": {
                "uncovered": uncovered_challenges,
                "under_addressed": under_addressed
            },
            "recommendations": self._generate_coverage_recommendations(coverage)
        }
    
    def _generate_coverage_recommendations(self, coverage: Dict[str, int]) -> List[str]:
        """Generate recommendations for improving solution coverage"""
        recommendations = []
        
        for challenge_name, solution_count in coverage.items():
            if solution_count == 0:
                recommendations.append(f"URGENT: Develop solutions for '{challenge_name}' - no current approaches")
            elif solution_count == 1:
                recommendations.append(f"Diversify solutions for '{challenge_name}' - only one approach available")
        
        return recommendations
    
    def get_implementation_roadmap(self) -> Dict[str, Any]:
        """Generate comprehensive implementation roadmap"""
        solution_roadmap = self.solutions.get_implementation_roadmap()
        challenge_priorities = self.challenges.get_priority_challenges()
        
        # Organize by urgency and feasibility
        roadmap = {
            "immediate_actions": [],
            "short_term_goals": [],
            "medium_term_objectives": [],
            "long_term_research": [],
            "challenge_priorities": [asdict(c) for c in challenge_priorities],
            "quick_wins": []
        }
        
        # Categorize solutions by urgency and impact
        quick_wins = self.solutions.get_quick_wins(6)  # 6 months
        high_impact = self.solutions.get_high_impact_solutions()
        
        roadmap["quick_wins"] = [asdict(s) for s in quick_wins if s in high_impact]
        
        for timeline, solutions in solution_roadmap.items():
            if "Short-term" in timeline:
                roadmap["short_term_goals"] = [asdict(s) for s in solutions]
            elif "Medium-term" in timeline:
                roadmap["medium_term_objectives"] = [asdict(s) for s in solutions]  
            elif "Long-term" in timeline or "Research" in timeline:
                roadmap["long_term_research"] = [asdict(s) for s in solutions]
        
        return roadmap
    
    def benchmark_current_state(self) -> Dict[str, Any]:
        """Benchmark current state of AI-SWE capabilities"""
        
        # Task distribution analysis
        task_distribution = self.framework.get_task_distribution()
        
        # Challenge severity analysis
        critical_challenges = self.challenges.get_challenges_by_severity(SeverityLevel.CRITICAL)
        high_challenges = self.challenges.get_challenges_by_severity(SeverityLevel.HIGH)
        
        # Solution readiness analysis
        solution_readiness = self.challenges.assess_system_readiness()
        
        # Overall readiness score
        overall_readiness = sum(solution_readiness.values()) / len(solution_readiness) if solution_readiness else 0
        
        return {
            "task_analysis": {
                "distribution": task_distribution,
                "total_tasks": len(self.framework.tasks),
                "coverage_gaps": self._identify_task_gaps(task_distribution)
            },
            "challenge_analysis": {
                "total_challenges": len(self.challenges.challenges),
                "critical_count": len(critical_challenges),
                "high_impact_count": len(high_challenges),
                "critical_challenges": [c.name for c in critical_challenges],
                "high_impact_challenges": [c.name for c in high_challenges]
            },
            "solution_readiness": solution_readiness,
            "overall_readiness": overall_readiness,
            "readiness_grade": self._grade_readiness(overall_readiness),
            "recommendations": self._generate_improvement_recommendations(overall_readiness, critical_challenges)
        }
    
    def _identify_task_gaps(self, distribution: Dict[str, Dict[str, int]]) -> List[str]:
        """Identify gaps in task coverage"""
        gaps = []
        
        # Check for underrepresented combinations
        scope_dist = distribution["scope"]
        complexity_dist = distribution["complexity"]
        
        if scope_dist.get("project", 0) < 2:
            gaps.append("Limited project-level task coverage")
        
        if complexity_dist.get("high", 0) < 2:
            gaps.append("Insufficient high-complexity task representation")
        
        return gaps
    
    def _grade_readiness(self, readiness_score: float) -> str:
        """Convert readiness score to letter grade"""
        if readiness_score >= 0.9:
            return "A (Excellent)"
        elif readiness_score >= 0.8:
            return "B (Good)"
        elif readiness_score >= 0.7:
            return "C (Fair)"
        elif readiness_score >= 0.6:
            return "D (Poor)"
        else:
            return "F (Critical)"
    
    def _generate_improvement_recommendations(self, readiness: float, critical_challenges: List[Challenge]) -> List[str]:
        """Generate recommendations for improving AI-SWE capabilities"""
        recommendations = []
        
        if readiness < 0.7:
            recommendations.append("URGENT: Address critical challenges to improve overall system capability")
        
        if len(critical_challenges) > 3:
            recommendations.append("Focus on top 3 critical challenges for maximum impact")
        
        for challenge in critical_challenges[:3]:
            solutions = self.solutions.get_solutions_for_challenge(challenge.name)
            if not solutions:
                recommendations.append(f"Develop solutions for critical challenge: {challenge.name}")
            else:
                feasible_solutions = [s for s in solutions if s.metrics.feasibility_score() > 0.5]
                if feasible_solutions:
                    recommendations.append(f"Prioritize implementation of {feasible_solutions[0].name}")
        
        return recommendations

async def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="AI for Software Engineering Framework - Evaluation & Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python evaluate.py --task "Function Completion"
  python evaluate.py --challenge-analysis
  python evaluate.py --roadmap
  python evaluate.py --benchmark
  python evaluate.py --claude-command analyze_task "Implement user authentication"
  python evaluate.py --list-tasks
  python evaluate.py --list-challenges --severity critical
        """
    )
    
    # Task evaluation
    parser.add_argument('--task', type=str, help='Evaluate a specific AI-SWE task')
    parser.add_argument('--scope', choices=['function', 'unit', 'project'], help='Filter by scope measure')
    parser.add_argument('--complexity', choices=['low', 'medium', 'high'], help='Filter by logical complexity')
    parser.add_argument('--intervention', choices=['low', 'medium', 'high'], help='Filter by human intervention level')
    
    # Challenge analysis
    parser.add_argument('--challenge-analysis', action='store_true', help='Analyze challenge coverage')
    parser.add_argument('--list-challenges', action='store_true', help='List all challenges')
    parser.add_argument('--severity', choices=['critical', 'high', 'medium', 'low'], help='Filter challenges by severity')
    
    # Solution analysis
    parser.add_argument('--roadmap', action='store_true', help='Generate implementation roadmap')
    parser.add_argument('--list-solutions', action='store_true', help='List all solutions')
    parser.add_argument('--quick-wins', type=int, default=12, help='Show quick wins (max months to deployment)')
    
    # Framework analysis
    parser.add_argument('--benchmark', action='store_true', help='Benchmark current AI-SWE state')
    parser.add_argument('--list-tasks', action='store_true', help='List all AI-SWE tasks')
    
    # Claude integration
    parser.add_argument('--claude-command', type=str, help='Execute a Claude Code command')
    parser.add_argument('--claude-help', type=str, help='Get help for a Claude command')
    parser.add_argument('--list-commands', action='store_true', help='List all Claude commands')
    
    # Output options
    parser.add_argument('--output', choices=['json', 'table', 'summary'], default='summary', help='Output format')
    parser.add_argument('--save', type=str, help='Save results to file')
    
    args = parser.parse_args()
    
    evaluator = FrameworkEvaluator()
    result = None
    
    try:
        # Task evaluation
        if args.task:
            result = evaluator.evaluate_task(args.task)
        
        # Challenge analysis
        elif args.challenge_analysis:
            result = evaluator.analyze_challenge_coverage()
        
        elif args.list_challenges:
            challenges = challenge_registry.challenges.values()
            if args.severity:
                severity_map = {
                    'critical': SeverityLevel.CRITICAL,
                    'high': SeverityLevel.HIGH,
                    'medium': SeverityLevel.MEDIUM,
                    'low': SeverityLevel.LOW
                }
                challenges = challenge_registry.get_challenges_by_severity(severity_map[args.severity])
            result = {"challenges": [asdict(c) for c in challenges]}
        
        # Solution analysis
        elif args.roadmap:
            result = evaluator.get_implementation_roadmap()
        
        elif args.list_solutions:
            solutions = solution_registry.solutions.values()
            result = {"solutions": [asdict(s) for s in solutions]}
        
        # Framework analysis
        elif args.benchmark:
            result = evaluator.benchmark_current_state()
        
        elif args.list_tasks:
            tasks = framework.tasks.values()
            if args.scope or args.complexity or args.intervention:
                scope_filter = ScopeMeasure(args.scope) if args.scope else None
                complexity_filter = LogicalComplexity(args.complexity) if args.complexity else None
                intervention_filter = HumanIntervention(args.intervention) if args.intervention else None
                tasks = framework.get_tasks_by_metrics(scope_filter, complexity_filter, intervention_filter)
            result = {"tasks": [asdict(t) for t in tasks]}
        
        # Claude integration
        elif args.claude_command:
            # Parse command and parameters (simplified)
            command_parts = args.claude_command.split()
            command_name = command_parts[0]
            # For demo purposes, using simple parameter parsing
            parameters = {"description": " ".join(command_parts[1:]) if len(command_parts) > 1 else ""}
            result = await claude_integration.execute_command(command_name, parameters)
        
        elif args.claude_help:
            help_text = claude_integration.get_command_help(args.claude_help)
            result = {"help": help_text}
        
        elif args.list_commands:
            commands = claude_integration.get_available_commands()
            result = {"commands": [{"name": c.name, "description": c.description, "category": c.category.value} for c in commands]}
        
        else:
            # Default: show framework overview
            result = {
                "framework_overview": {
                    "total_tasks": len(framework.tasks),
                    "total_challenges": len(challenge_registry.challenges),
                    "total_solutions": len(solution_registry.solutions),
                    "claude_commands": len(claude_integration.commands)
                },
                "quick_stats": evaluator.benchmark_current_state()
            }
        
        # Output results
        if result:
            output_result(result, args.output, args.save)
        else:
            print("No operation specified. Use --help for usage information.")
            
    except Exception as e:
        logger.error(f"Error during evaluation: {e}")
        print(f"Error: {e}")
        sys.exit(1)

def output_result(result: Dict[str, Any], format_type: str, save_path: Optional[str] = None):
    """Output results in specified format"""
    
    if format_type == 'json':
        output = json.dumps(result, indent=2, default=str)
    elif format_type == 'table':
        output = format_as_table(result)
    else:  # summary
        output = format_as_summary(result)
    
    if save_path:
        Path(save_path).write_text(output, encoding='utf-8')
        print(f"Results saved to {save_path}")
    else:
        print(output)

def format_as_table(result: Dict[str, Any]) -> str:
    """Format result as table (simplified)"""
    # This would implement proper table formatting
    return json.dumps(result, indent=2, default=str)

def format_as_summary(result: Dict[str, Any]) -> str:
    """Format result as human-readable summary"""
    summary = []
    
    # Framework overview
    if "framework_overview" in result:
        overview = result["framework_overview"]
        summary.append("🚀 AI for Software Engineering Framework")
        summary.append("=" * 50)
        summary.append(f"📋 Tasks: {overview['total_tasks']}")
        summary.append(f"⚠️  Challenges: {overview['total_challenges']}")
        summary.append(f"💡 Solutions: {overview['total_solutions']}")
        summary.append(f"🤖 Claude Commands: {overview['claude_commands']}")
        summary.append("")
    
    # Task evaluation
    if "task" in result:
        task = result["task"]
        summary.append(f"📝 Task: {task['name']}")
        summary.append(f"Category: {task['category']}")
        summary.append(f"Scope: {task['metrics']['scope']}")
        summary.append(f"Complexity: {task['metrics']['complexity']}")
        summary.append(f"Intervention: {task['metrics']['intervention']}")
        summary.append(f"Readiness Score: {result.get('readiness_score', 0):.2f}")
        summary.append(f"Recommendation: {result.get('recommendation', 'N/A')}")
        summary.append("")
    
    # Challenge analysis
    if "coverage_percentage" in result:
        summary.append(f"📊 Challenge Coverage Analysis")
        summary.append(f"Coverage: {result['coverage_percentage']:.1f}%")
        summary.append(f"Covered: {result['covered_challenges']}/{result['total_challenges']}")
        if result['gaps']['uncovered']:
            summary.append(f"❌ Uncovered: {', '.join(result['gaps']['uncovered'])}")
        summary.append("")
    
    # Benchmark results
    if "overall_readiness" in result:
        summary.append(f"📈 Framework Readiness: {result['readiness_grade']}")
        summary.append(f"Score: {result['overall_readiness']:.2f}")
        if result.get('recommendations'):
            summary.append("🎯 Recommendations:")
            for rec in result['recommendations'][:3]:
                summary.append(f"  • {rec}")
        summary.append("")
    
    return "\n".join(summary)

if __name__ == "__main__":
    asyncio.run(main()) 