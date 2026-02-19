import os
import base64
import json
from google import genai
from groq import Groq
from google.genai import types
import httpx
from dotenv import load_dotenv

load_dotenv()

# Setup Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Hugging Face Settings
HF_TOKEN = os.getenv("HF_API_KEY")
SD_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
HF_API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell" 
HF_TOKEN = os.getenv("HF_API_KEY")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def generate_strategic_guidance(idea: str, industry: str):
    """Uses Groq (Llama-3) to provide strategic branding guidance as a stable fallback for Granite."""
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a strategic brand consultant specialized in the IBM Granite framework. Provide a professional strategy report. Return ONLY the report text."},
                {"role": "user", "content": f"Brand: {idea}\nIndustry: {industry}\n\nProvide: 1. Brand Archetype, 2. Strategic Positioning, 3. Three consultative questions to help the founder."}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Strategic Guidance Error: {e}")
        return "Our strategic consultant is currently busy refining visions. Focus on your core values and target audience to build a strong foundation."

async def generate_brand_details(user_idea: str):
    """Uses Groq to generate brand details."""
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a branding expert. Return ONLY JSON with 'names' (list of 3), 'tagline', 'visual_vibe', 'logo_prompt'. In 'logo_prompt', include instructions for bold, clear typography and high contrast vector style."},
                {"role": "user", "content": f"Brand Idea: {user_idea}"}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"Groq Error: {e}")
        return {
            "names": [f"{user_idea} Studio", f"{user_idea} Co", f"Pure {user_idea}"],
            "tagline": "Simplifying your vision",
            "visual_vibe": "Minimalist and modern",
            "logo_prompt": f"A high-contrast vector logo for a company called {user_idea}, featuring bold, clear, and perfectly spelled typography on a clean background."
        }

async def generate_logo(prompt: str, filename: str):
    """Calls Hugging Face to generate a logo and saves it to frontend/static/generated_logos."""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # Refining the prompt for clarity and typography
    refined_prompt = f"{prompt}. Highly detailed, sharp edges, professional branding, clear typography, centered, vector logo style, flat colors, no blur, high resolution."
    
    # Path relative to backend/main.py
    logo_dir = os.path.join("..", "frontend", "static", "generated_logos")
    os.makedirs(logo_dir, exist_ok=True)
    save_path = os.path.join(logo_dir, filename)
    
    async with httpx.AsyncClient() as http_client:
        try:
            # Fixing the payload for HF Inference API
            response = await http_client.post(
                HF_API_URL,
                headers=headers,
                json={"inputs": refined_prompt}, 
                timeout=60.0
            )

            
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                return f"/static/generated_logos/{filename}"
            else:
                print(f"Hugging Face Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error generating logo: {e}")
            
        return "/static/placeholder_logo.png"

async def generate_marketing_content(description: str, tone: str, content_type: str):
    """Generates marketing copy using Groq."""
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"Write a {tone} {content_type}. Return ONLY the text content."},
                {"role": "user", "content": f"Brand Description: {description}"}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Groq Content Error: {e}")
        return f"Explore our {tone} {content_type} for your unique brand journey."

async def generate_design_system(idea: str):
    """Generates a color palette and font pairing using Groq."""
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Generate a design system. Return ONLY JSON with these exact keys: 'primary_color', 'secondary_color', 'accent_color', 'font_pairing'."},
                {"role": "user", "content": f"Brand Idea: {idea}"}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"Groq Design Error: {e}")
        return {
            "primary_color": "#6366f1",
            "secondary_color": "#a855f7",
            "accent_color": "#f59e0b",
            "font_pairing": "Inter & Roboto"
        }

async def analyze_review(review_text: str):
    """Analyzes customer review sentiment and provides a professional rewrite/response using Groq."""
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a customer success expert. Analyze the sentiment (Positive/Negative/Neutral), identify key points, and provide a polite, professional 'Diplomatic Response' to this review. Return ONLY the text report."},
                {"role": "user", "content": f"Review: {review_text}"}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Review Analysis Error: {e}")
        return "Sentiment: Analysis Pending. Advice: Always respond with empathy and clarity to customer feedback."

async def chat_response(user_message: str):
    """Generates a conversational branding consultant response using Groq."""
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a world-class AI Branding Consultant for BizForge. Be concise, expert, and encouraging. Answer questions about logos, branding, marketing, and design. Return ONLY the message content."},
                {"role": "user", "content": user_message}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Chat Error: {e}")
        return "I'm currently contemplating the perfect brand strategy. Ask me something about design or identity!"
