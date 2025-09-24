# infrastructure/ai_service.py

import openai
import os
from dotenv import load_dotenv
from infrastructure.logger import logger

# Load environment variables
load_dotenv()

class AIService:
    """
    AI service using GPT-4 to check for abusive and sexual content.
    """
    
    def __init__(self):
        # Initialize OpenAI client
        self.client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        # Enhanced fallback keyword filtering (English, Hindi, Punjabi)
        self.abusive_keywords = [
            # English sexual/inappropriate
            'sex', 'fuck', 'shit', 'bitch', 'ass', 'dick', 'pussy', 'boobs', 'nude', 'naked', 'i want sex', 'sex with you',
            'porn', 'horny', 'sexy', 'kiss', 'love', 'date', 'marry', 'girlfriend', 'boyfriend',
            # English abusive
            'hate', 'kill', 'die', 'stupid', 'idiot', 'moron', 'dumb', 'ugly', 'fat',
            'threat', 'violence', 'harm', 'hurt', 'attack', 'destroy', 'abuse', 'harass', 'bully',
            # Hindi/Devanagari inappropriate
            'सेक्स', 'चुदाई', 'रंडी', 'भोसड़ी', 'गांड', 'लंड', 'चूत', 'मादरचोद', 'भेनचोद',
            'कुत्ता', 'कुतिया', 'हरामी', 'साला', 'बहनचोद', 'गधा', 'उल्लू',
            # Punjabi inappropriate (Gurmukhi)
            'ਸੈਕਸ', 'ਚੁਦਾਈ', 'ਰੰਡੀ', 'ਭੋਸੜੀ', 'ਗੰਡ', 'ਲੰਡ', 'ਚੂਤ', 'ਮਾਦਰਚੋਦ',
            'ਕੁੱਤਾ', 'ਕੁੱਤੀ', 'ਹਰਾਮੀ', 'ਸਾਲਾ', 'ਬਹਿਣਚੋਦ'
        ]
        logger.info("AI Service initialized with GPT-4 content filtering.")
    
    def check_for_abuse(self, content: str) -> bool:
        """
        Checks if the content is inappropriate using GPT-4.
        Returns True if abusive content is detected, False otherwise.
        """
        try:
            # First try GPT-4 moderation
            if self.client.api_key:
                return self._check_with_gpt4(content)
            else:
                logger.warning("OpenAI API key not found, using fallback filtering")
                return self._fallback_check(content)
                
        except Exception as e:
            logger.error(f"Error in AI content check: {e}")
            # Fallback to keyword filtering
            return self._fallback_check(content)
    
    def _check_with_gpt4(self, content: str) -> bool:
        """
        Use GPT-4 to analyze content for inappropriate material.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a strict content moderator. Analyze the following message in ANY language (English, Hindi, Punjabi, or any other language) and determine if it contains ANY abusive, sexual, threatening, harassing, inappropriate, vulgar, or offensive content. This includes sexual requests, abuse, threats, harassment, vulgar language, or any inappropriate behavior. Be VERY STRICT. Respond with only 'UNSAFE' if the content is inappropriate in ANY way, or 'SAFE' if it is completely appropriate and respectful."
                    },
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                max_tokens=10,
                temperature=0
            )
            
            result = response.choices[0].message.content.strip().upper()
            is_unsafe = result == 'UNSAFE'
            
            if is_unsafe:
                logger.warning(f"GPT-4 flagged inappropriate content: {result}")
            else:
                logger.info("Content passed GPT-4 moderation check.")
                
            return is_unsafe
            
        except Exception as e:
            logger.error(f"GPT-4 moderation failed: {e}")
            return self._fallback_check(content)
    
    def _fallback_check(self, content: str) -> bool:
        """
        Fallback keyword-based filtering.
        """
        content_lower = content.lower()
        
        for keyword in self.abusive_keywords:
            if keyword in content_lower:
                logger.warning(f"Fallback filter detected inappropriate content: contains '{keyword}'")
                return True
        
        logger.info("Content passed fallback moderation check.")
        return False
