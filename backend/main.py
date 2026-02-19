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
    logo_url = f"/static/generated_logos/{logo_filename}"
    await generate_logo(f"A logo for {name}, {keywords}", logo_filename)
    
    html_content = f"""
    <div class="main-logo-card">
        <h3 style="color: var(--accent); margin-bottom: 2rem; font-size: 1.8rem; font-weight: 800;">Logo Forged</h3>
        <div class="logo-display">
            <img src="{logo_url}" id="forged-logo-img" style="width: 280px; transition: all 0.5s ease;">
        </div>
        <p style="color: rgba(255,255,255,0.7); font-size: 1.1rem; margin-bottom: 2.5rem;">Concept for: <strong style="color: white; font-weight: 700;">{name}</strong></p>
        
        <div class="lab-actions">
            <a href="{logo_url}" download="BizForge_Logo_{name}.png" class="btn-crystal btn-crystal-accent">
                📥 Download Logo
            </a>
            <button onclick="toggleLogoLab()" class="btn-crystal btn-crystal-glass">
                🎨 Open Logo Lab
            </button>
        </div>
    </div>

    <!-- BizForge Logo Lab (Crystal Manual Modifier) -->
    <div id="logo-lab" class="logo-lab" style="display: none;">
        <div class="lab-header">
            <h4>Logo Studio Lab</h4>
            <p style="color: rgba(255,255,255,0.4); font-size: 0.9rem; margin-top: 0.5rem;">Manual modification & fine-tuning</p>
        </div>
        
        <div class="lab-layout">
            <div class="lab-preview-container">
                <div id="lab-wrapper" class="lab-image-wrapper">
                    <img src="{logo_url}" id="lab-preview-img" class="lab-img">
                    <div id="lab-text-overlay" class="lab-text-overlay"></div>
                </div>
            </div>
            
            <div class="lab-controls">
                <div class="control-item">
                    <label>Add Tagline / Text</label>
                    <input type="text" id="lab-tagline-input" class="lab-input" oninput="updateLabText(this.value)" placeholder="Type your tagline...">
                </div>
                
                <div class="control-item">
                    <label>Color Shift (Hue)</label>
                    <input type="range" min="0" max="360" value="0" class="lab-slider" oninput="updateLabFilters()">
                </div>
                
                <div class="control-item">
                    <label>Brightness</label>
                    <input type="range" min="50" max="250" value="100" class="lab-slider" oninput="updateLabFilters()">
                </div>
                
                <div class="control-item">
                    <label>Frame Expression</label>
                    <div class="shape-buttons">
                        <button class="btn-shape" id="shape-square" onclick="updateLabShape('square')">Square</button>
                        <button class="btn-shape" id="shape-rounded" onclick="updateLabShape('rounded')">Rounded</button>
                        <button class="btn-shape" id="shape-circle" onclick="updateLabShape('circle')">Circle</button>
                    </div>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 2rem; padding: 1.5rem; background: rgba(0,0,0,0.2); border-radius: 16px; border-left: 4px solid var(--accent);">
            <p style="font-size: 0.85rem; color: rgba(255,255,255,0.6); line-height: 1.4;">
                💡 <strong>Tip:</strong> Manual modifications are applied instantly. Once satisfied, right-click the preview image and select <strong>"Save Image As"</strong> to export your customized brand asset.
            </p>
        </div>
    </div>

    <script>
        function toggleLogoLab() {{
            const lab = document.getElementById('logo-lab');
            lab.style.display = lab.style.display === 'none' ? 'block' : 'none';
            if(lab.style.display === 'block') {{
                lab.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}
        }}

        function updateLabText(val) {{
            document.getElementById('lab-text-overlay').innerText = val;
        }}

        function updateLabFilters() {{
            const hue = document.querySelectorAll('.lab-slider')[0].value;
            const bright = document.querySelectorAll('.lab-slider')[1].value;
            document.getElementById('lab-preview-img').style.filter = `hue-rotate(${{hue}}deg) brightness(${{bright}}%)`;
        }}

        function updateLabShape(shape) {{
            const wrapper = document.getElementById('lab-wrapper');
            wrapper.className = 'lab-image-wrapper ' + shape;
            
            // Toggle active state for buttons
            document.querySelectorAll('.btn-shape').forEach(btn => btn.classList.remove('active'));
            document.getElementById('shape-' + shape).classList.add('active');
        }}
    </script>
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
    primary = design.get('primary_color', '#6366f1')
    secondary = design.get('secondary_color', '#a855f7')
    accent = design.get('accent_color', '#f59e0b')
    font = design.get('font_pairing', 'Inter & Roboto')

    html_content = f"""
    <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 16px;">
        <h3 style="color: var(--accent); margin-bottom: 1.5rem;">Design System: {idea}</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
            <div style="text-align: center;">
                <div style="height: 60px; background: {primary}; border-radius: 8px; margin-bottom: 0.5rem;"></div>
                <p style="font-size: 0.8rem;">Primary: {primary}</p>
            </div>
            <div style="text-align: center;">
                <div style="height: 60px; background: {secondary}; border-radius: 8px; margin-bottom: 0.5rem;"></div>
                <p style="font-size: 0.8rem;">Secondary: {secondary}</p>
            </div>
            <div style="text-align: center;">
                <div style="height: 60px; background: {accent}; border-radius: 8px; margin-bottom: 0.5rem;"></div>
                <p style="font-size: 0.8rem;">Accent: {accent}</p>
            </div>
        </div>
        <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 8px;">
            <p><strong>Font Pairing:</strong> {font}</p>
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

def format_chat_response(text):
    import re
    # Bold: **text** -> <strong>text</strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Lists: 1. -> <br>1.
    text = re.sub(r'(\d+\.)', r'<br>\1', text)
    return text

@app.post("/api/chat")
async def api_chat(request: Request, message: str = Form(...)):
    response = await chat_response(message)
    formatted_response = format_chat_response(response)
    # Premium chat bubbles with avatars
    html_content = f"""
    <div class="chat-message user">
        <div class="avatar">👤</div>
        <div class="message-bubble">{message}</div>
    </div>
    <div class="chat-message ai">
        <div class="avatar">🤖</div>
        <div class="message-bubble">{formatted_response}</div>
    </div>
    <script>
        (function() {{
            const win = document.querySelector('.chat-window');
            if (win) win.scrollTop = win.scrollHeight;
        }})();
    </script>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)