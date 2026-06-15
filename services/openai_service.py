"""
OpenAI API integration service.
"""

from typing import Optional
import os

import openai
from openai import OpenAI, APIError

from utils.logger import setup_logger
from config.settings import get_settings

logger = setup_logger(__name__)
settings = get_settings()


class OpenAIService:
    """
    Manages OpenAI API communication.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI service.
        
        Args:
            api_key: OpenAI API key (uses env var if not provided)
        
        Raises:
            ValueError: If API key is not provided or found
        """
        key = api_key or os.getenv("OPENAI_API_KEY") or settings.openai_api_key
        
        if not key:
            raise ValueError(
                "OpenAI API key not provided. "
                "Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )
        
        self.client = OpenAI(api_key=key)
        self.model = settings.openai_model
        logger.info(f"OpenAI service initialized with model: {self.model}")
    
    def call_api(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7,
    ) -> str:
        """
        Call OpenAI API with a prompt.
        
        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-2)
        
        Returns:
            API response text
        
        Raises:
            ValueError: If API call fails
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI tutor helping students improve their academic assignments."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            
            result = response.choices[0].message.content
            logger.info("OpenAI API call successful")
            return result
        
        except APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise ValueError(f"OpenAI API error: {str(e)}")
        
        except Exception as e:
            logger.error(f"Unexpected error calling OpenAI API: {str(e)}")
            raise ValueError(f"Unexpected error: {str(e)}")
    
    def analyze_text(
        self,
        text: str,
        analysis_type: str = "general",
    ) -> str:
        """
        Analyze academic text.
        
        Args:
            text: Text to analyze
            analysis_type: Type of analysis
        
        Returns:
            Analysis result
        """
        analysis_prompts = {
            "general": f"분석해주세요: {text}",
            "grammar": f"문법을 검토해주세요: {text}",
            "structure": f"구조와 흐름을 분석해주세요: {text}",
            "content": f"내용의 정확성과 깊이를 평가해주세요: {text}",
        }
        
        prompt = analysis_prompts.get(analysis_type, analysis_prompts["general"])
        return self.call_api(prompt)
