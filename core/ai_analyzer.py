"""
AI-based analysis of academic assignments and performance.

Handles communication with OpenAI API and feedback generation.
"""

from typing import Optional, Dict, Any
import json
from datetime import datetime

from services.openai_service import OpenAIService
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AIAnalyzer:
    """
    Analyzes academic assignments using AI.
    """
    
    def __init__(self, openai_service: OpenAIService):
        """
        Initialize AIAnalyzer.
        
        Args:
            openai_service: OpenAI service instance
        """
        self.openai_service = openai_service
    
    def analyze_assignment(
        self,
        assignment_text: str,
        assignment_type: str = "general",
    ) -> Dict[str, Any]:
        """
        Analyze an academic assignment and provide feedback.
        
        Args:
            assignment_text: The assignment text to analyze
            assignment_type: Type of assignment ('essay', 'presentation', 'report', etc.)
        
        Returns:
            Dictionary with analysis results
        
        Raises:
            ValueError: If API call fails
        """
        try:
            prompt = self._build_analysis_prompt(assignment_text, assignment_type)
            response = self.openai_service.call_api(prompt)
            
            analysis = self._parse_response(response)
            logger.info(f"Assignment analyzed successfully")
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error analyzing assignment: {str(e)}")
            raise ValueError(f"Failed to analyze assignment: {str(e)}")
    
    def get_improvement_suggestions(
        self,
        assignment_text: str,
        current_score: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get specific improvement suggestions for an assignment.
        
        Args:
            assignment_text: The assignment text
            current_score: Optional current score (0-100)
        
        Returns:
            Dictionary with suggestions
        """
        try:
            prompt = self._build_suggestions_prompt(assignment_text, current_score)
            response = self.openai_service.call_api(prompt)
            
            suggestions = self._parse_suggestions(response)
            logger.info("Improvement suggestions generated")
            
            return suggestions
        
        except Exception as e:
            logger.error(f"Error generating suggestions: {str(e)}")
            raise ValueError(f"Failed to generate suggestions: {str(e)}")
    
    def _build_analysis_prompt(self, text: str, assignment_type: str) -> str:
        """
        Build the analysis prompt for OpenAI.
        
        Args:
            text: Assignment text
            assignment_type: Type of assignment
        
        Returns:
            Formatted prompt
        """
        return f"""
        다음 {assignment_type} 과제를 분석하고 평가해주세요.
        구조, 내용, 논리성을 중점적으로 평가하세요.
        
        과제:
        {text}
        
        다음 JSON 형식으로 응답해주세요:
        {{
            "overall_score": 0-100,
            "strengths": ["강점1", "강점2"],
            "weaknesses": ["약점1", "약점2"],
            "summary": "전체 평가 요약"
        }}
        """
    
    def _build_suggestions_prompt(
        self,
        text: str,
        score: Optional[int] = None,
    ) -> str:
        """
        Build the improvement suggestions prompt.
        
        Args:
            text: Assignment text
            score: Optional current score
        
        Returns:
            Formatted prompt
        """
        score_context = f"현재 점수: {score}점" if score else "현재 점수: 미정"
        
        return f"""
        다음 과제를 개선하기 위한 구체적인 제안을 주세요.
        {score_context}
        
        과제:
        {text}
        
        다음 JSON 형식으로 응답해주세요:
        {{
            "improvements": [
                {{
                    "area": "개선 영역",
                    "current_issue": "현재 문제점",
                    "suggestion": "구체적인 개선안",
                    "priority": "high|medium|low"
                }}
            ],
            "estimated_new_score": 0-100
        }}
        """
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse JSON response from OpenAI.
        
        Args:
            response: Raw response text
        
        Returns:
            Parsed dictionary
        """
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON response, returning raw text")
            return {"raw_response": response}
    
    def _parse_suggestions(self, response: str) -> Dict[str, Any]:
        """
        Parse improvement suggestions from response.
        
        Args:
            response: Raw response text
        
        Returns:
            Parsed suggestions dictionary
        """
        return self._parse_response(response)
