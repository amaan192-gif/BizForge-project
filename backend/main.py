import os
import json
import httpx
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# Import the AI functions
from ai_services import (
    generate_brand_details, 
    generate_logo, 
    generate_marketing_content, 
    generate_design_system,
    generate_strategic_guidance,
    analyze_review,
    chat_response
)

load_dotenv()

app = FastAPI(title="BizForge AI Branding Suite")

# Mount static files
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="../frontend")

@app.get("/")
@app.get("/index.html")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/branding.html")
async def branding(request: Request):
    return templates.TemplateResponse("branding.html", {"request": request})

@app.post("/api/brand")
async def api_brand(request: Request, idea: str = Form(...), industry: str = Form("Technology"), tone: str = Form("Professional")):
    brand_data = await generate_brand_details(f"{idea} in {industry} industry with a {tone} tone")
    logo_filename = f"logo_{os.urandom(4).hex()}.png"
    logo_url = await generate_logo(brand_data['logo_prompt'], logo_filename)
    names_html = "".join([f"<li style='background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; list-style: none;'>✨ {name}</li>" for name in brand_data['names']])
    
    html_content = f"""
    <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 16px; border: 1px solid var(--primary);">
        <div style="display: flex; gap: 2rem; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 300px;">
                <h3 style="color: var(--accent); margin-bottom: 1rem;">Forged Identities</h3>
                <ul style="margin-bottom: 1.5rem;">{names_html}</ul>
                <p style="font-style: italic; color: rgba(255,255,255,0.8);">"{brand_data['tagline']}"</p>
                <p style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.7;">Vibe: {brand_data['visual_vibe']}</p>
            </div>
            <div style="width: 200px;">
                <h3 style="color: var(--accent); margin-bottom: 1rem;">Logo Concept</h3>
                <img src="{logo_url}" style="width: 100%; border-radius: 12px; background: white; padding: 10px;">
            </div>
        </div>
    </div>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/logo")
async def api_logo(request: Request, name: str = Form(...), keywords: str = Form("modern, minimalist, tech")):
    logo_filename = f"logo_{os.urandom(4).hex()}.png"
    logo_url = await generate_logo(f"A logo for {name}, {keywords}", logo_filename)
    html_content = f"""
    <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 16px; text-align: center;">
        <h3 style="color: var(--accent); margin-bottom: 1rem;">Logo Forged</h3>
        <img src="{logo_url}" style="width: 250px; border-radius: 12px; background: white; padding: 10px; margin-bottom: 1rem;">
        <p style="color: rgba(255,255,255,0.8);">Concept for: <strong>{name}</strong></p>
    </div>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/content")
async def api_content(request: Request, description: str = Form(...), tone: str = Form("Professional"), content_type: str = Form("Product Description")):
    content = await generate_marketing_content(description, tone, content_type)
    html_content = f"""
    <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 16px;">
        <h3 style="color: var(--accent); margin-bottom: 1rem;">{content_type}</h3>
        <div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 8px; line-height: 1.6; white-space: pre-wrap;">
            {content}
        </div>
    </div>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/design")
async def api_design(request: Request, idea: str = Form(...)):
    design = await generate_design_system(idea)
    html_content = f"""
    <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 16px;">
        <h3 style="color: var(--accent); margin-bottom: 1.5rem;">Design System: {idea}</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
            <div style="text-align: center;">
                <div style="height: 60px; background: {design['primary_color']}; border-radius: 8px; margin-bottom: 0.5rem;"></div>
                <p style="font-size: 0.8rem;">Primary: {design['primary_color']}</p>
            </div>
            <div style="text-align: center;">
                <div style="height: 60px; background: {design['secondary_color']}; border-radius: 8px; margin-bottom: 0.5rem;"></div>
                <p style="font-size: 0.8rem;">Secondary: {design['secondary_color']}</p>
            </div>
            <div style="text-align: center;">
                <div style="height: 60px; background: {design['accent_color']}; border-radius: 8px; margin-bottom: 0.5rem;"></div>
                <p style="font-size: 0.8rem;">Accent: {design['accent_color']}</p>
            </div>
        </div>
        <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 8px;">
            <p><strong>Font Pairing:</strong> {design['font_pairing']}</p>
        </div>
    </div>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/consultant")
async def api_consultant(request: Request, idea: str = Form(...), industry: str = Form("Technology")):
    guidance = await generate_strategic_guidance(idea, industry)
    html_content = f"""
    <div style="background: rgba(255,255,255,0.1); padding: 2.5rem; border-radius: 24px; border: 1px solid var(--accent);">
        <h3 style="color: var(--accent); margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.75rem;">
            <span>🤖</span> Strategic Consultant Report
        </h3>
        <div style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 16px; line-height: 1.8; color: #fff; font-size: 1.05rem; white-space: pre-wrap;">
            {guidance}
        </div>
        <div style="margin-top: 2rem; padding: 1rem; border-left: 4px solid var(--accent); background: rgba(245, 158, 11, 0.1); border-radius: 0 8px 8px 0;">
            <p style="font-size: 0.9rem; color: var(--accent); font-weight: 600;">Powered by IBM Granite Strategy Engine (via Groq Fallback)</p>
        </div>
    </div>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/analyze")
async def api_analyze(request: Request, review: str = Form(...)):
    analysis = await analyze_review(review)
    # Wrap analysis in a premium container
    html_content = f"""
    <div class="analysis-report">
        <h4><span>🔍</span> Review Insights & Professional Strategy</h4>
        <div class="analysis-body">
            {analysis}
        </div>
        <div class="analysis-footer">
            <p>Analyzed by BizForge Sentiment Engine</p>
        </div>
    </div>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/chat")
async def api_chat(request: Request, message: str = Form(...)):
    response = await chat_response(message)
    # Premium chat bubbles with avatars
    html_content = f"""
    <div class="chat-message user">
        <div class="avatar">👤</div>
        <div class="message-bubble">{message}</div>
    </div>
    <div class="chat-message ai">
        <div class="avatar">🤖</div>
        <div class="message-bubble">{response}</div>
    </div>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)