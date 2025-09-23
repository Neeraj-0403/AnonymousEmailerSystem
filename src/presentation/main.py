# presentation/main.py

import sys
import os
import time
import threading
import streamlit as st
import pygame
from io import BytesIO
import base64

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application.auth_service import AuthService
from application.email_service import EmailService
from infrastructure.excel_repository import ExcelRepository
from infrastructure.ai_service import AIService
from infrastructure.encryption_service import EncryptionService
from infrastructure.logger import setup_logger, logger

# Initialize pygame mixer for sound
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    SOUND_ENABLED = True
except:
    SOUND_ENABLED = False
    logger.warning("Sound system not available")

# Sound functions
def play_keypress_sound():
    if not SOUND_ENABLED or not st.session_state.get('sound_enabled', True):
        return
    try:
        # Generate a simple beep sound
        duration = 0.1
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []
        for i in range(frames):
            wave = 4096 * (i % (sample_rate // 800) < (sample_rate // 1600))
            arr.append([wave, wave])
        sound = pygame.sndarray.make_sound(arr)
        sound.play()
    except Exception as e:
        logger.error(f"Sound error: {e}")

def play_welcome_sound():
    if not SOUND_ENABLED or not st.session_state.get('sound_enabled', True):
        return
    try:
        # Play a welcome melody
        notes = [523, 659, 784, 1047]  # C5, E5, G5, C6
        for i, freq in enumerate(notes):
            threading.Timer(i * 0.3, lambda f=freq: play_note(f)).start()
    except Exception as e:
        logger.error(f"Sound error: {e}")

def play_note(frequency):
    try:
        duration = 0.4
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []
        for i in range(frames):
            wave = int(4096 * (i % (sample_rate // frequency) < (sample_rate // (frequency * 2))))
            arr.append([wave, wave])
        sound = pygame.sndarray.make_sound(arr)
        sound.play()
    except:
        pass

# --- Initialization (services) ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.authenticated = False
    st.session_state.sound_enabled = True

    try:
        encryption_service = EncryptionService()
        st.session_state.ai_service = AIService()
        st.session_state.excel_repository = ExcelRepository(
            auth_file='auth_codes.xlsx',
            email_file='emails_to_send.xlsx',
            encryption_service=encryption_service
        )
        st.session_state.auth_service = AuthService(auth_repository=st.session_state.excel_repository)
        st.session_state.email_service = EmailService(
            email_repository=st.session_state.excel_repository,
            ai_service=st.session_state.ai_service
        )
    except Exception as e:
        st.error(f"⚠️ Failed to initialize. Ensure `secret.key` and Excel files exist. Error: {e}")
        st.stop()

# --- Streamlit UI Setup ---
st.set_page_config(
    page_title="🎆 Anonymous Diwali Mailer", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- Bootstrap & Custom CSS ---
st.markdown("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    
    <style>
    body {
        font-family: 'Orbitron', monospace;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        margin: 0;
        padding: 0;
    }
    
    .stApp {
        background: transparent !important;
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        margin: 20px;
        padding: 30px;
    }
    
    .diwali-card {
        background: linear-gradient(145deg, rgba(255, 165, 0, 0.1), rgba(255, 215, 0, 0.1));
        border: 2px solid rgba(255, 165, 0, 0.3);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 25px rgba(255, 165, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .diwali-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(255, 165, 0, 0.3);
    }
    
    .btn-diwali {
        background: linear-gradient(45deg, #ff6b35, #f7931e, #ffcc02);
        border: none;
        color: white;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-radius: 25px;
        padding: 12px 30px;
        box-shadow: 0 6px 20px rgba(255, 165, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .btn-diwali:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 10px 30px rgba(255, 165, 0, 0.6);
        color: white;
    }
    
    .form-control {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(255, 152, 0, 0.3);
        border-radius: 15px;
        padding: 15px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .form-control:focus {
        background: rgba(255, 255, 255, 0.95);
        border-color: #ff9800;
        box-shadow: 0 0 20px rgba(255, 165, 0, 0.4);
    }
    
    .title-glow {
        background: linear-gradient(45deg, #ff6b35, #f7931e, #ffcc02, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.8);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 20px rgba(255,215,0,0.5)); }
        to { filter: drop-shadow(0 0 30px rgba(255,215,0,0.8)); }
    }
    
    .sound-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: linear-gradient(45deg, #4CAF50, #45a049);
        border: none;
        color: white;
        padding: 12px 20px;
        border-radius: 25px;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        transition: all 0.3s ease;
    }
    
    .sound-toggle:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.5);
    }
    
    .fireworks-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        pointer-events: none;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #667eea 100%);
    }
    
    .celebration-alert {
        background: linear-gradient(45deg, rgba(76, 175, 80, 0.3), rgba(139, 195, 74, 0.3));
        border: 3px solid #4caf50;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(76, 175, 80, 0.3);
        animation: pulse 1s ease-in-out;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .stButton button {
        background: linear-gradient(45deg, #ff6b35, #f7931e, #ffcc02) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 30px !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 6px 20px rgba(255, 165, 0, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) scale(1.05) !important;
        box-shadow: 0 10px 30px rgba(255, 165, 0, 0.6) !important;
    }
    
    .stTextInput input, .stTextArea textarea {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(255, 152, 0, 0.3) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        font-size: 16px !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #ff9800 !important;
        box-shadow: 0 0 20px rgba(255, 165, 0, 0.4) !important;
    }
    </style>
</head>
<body>
    <canvas id="fireworksCanvas" class="fireworks-bg"></canvas>
    
    <button class="sound-toggle" onclick="toggleSound()" id="soundBtn">
        <i class="fas fa-volume-up"></i> Sound ON
    </button>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
    let soundEnabled = true;
    
    function toggleSound() {
        soundEnabled = !soundEnabled;
        const btn = document.getElementById('soundBtn');
        if (soundEnabled) {
            btn.innerHTML = '<i class="fas fa-volume-up"></i> Sound ON';
            btn.style.background = 'linear-gradient(45deg, #4CAF50, #45a049)';
        } else {
            btn.innerHTML = '<i class="fas fa-volume-mute"></i> Sound OFF';
            btn.style.background = 'linear-gradient(45deg, #f44336, #d32f2f)';
        }
    }
    
    // Fireworks Animation
    class Firework {
        constructor(x, y, targetX, targetY) {
            this.x = x;
            this.y = y;
            this.targetX = targetX;
            this.targetY = targetY;
            this.speed = 5;
            this.angle = Math.atan2(targetY - y, targetX - x);
            this.brightness = Math.random() * 360;
            this.exploded = false;
            this.particles = [];
        }
        
        update() {
            if (!this.exploded) {
                this.x += Math.cos(this.angle) * this.speed;
                this.y += Math.sin(this.angle) * this.speed;
                
                if (Math.abs(this.x - this.targetX) < 10 && Math.abs(this.y - this.targetY) < 10) {
                    this.explode();
                }
            } else {
                this.particles.forEach(p => p.update());
                this.particles = this.particles.filter(p => p.alpha > 0);
            }
        }
        
        explode() {
            this.exploded = true;
            for (let i = 0; i < 30; i++) {
                this.particles.push(new Particle(this.x, this.y, this.brightness));
            }
        }
        
        draw(ctx) {
            if (!this.exploded) {
                ctx.fillStyle = `hsl(${this.brightness}, 100%, 60%)`;
                ctx.beginPath();
                ctx.arc(this.x, this.y, 3, 0, Math.PI * 2);
                ctx.fill();
            } else {
                this.particles.forEach(p => p.draw(ctx));
            }
        }
    }
    
    class Particle {
        constructor(x, y, hue) {
            this.x = x;
            this.y = y;
            this.vx = (Math.random() - 0.5) * 8;
            this.vy = (Math.random() - 0.5) * 8;
            this.alpha = 1;
            this.decay = Math.random() * 0.02 + 0.01;
            this.hue = hue + Math.random() * 60 - 30;
        }
        
        update() {
            this.x += this.vx;
            this.y += this.vy;
            this.vy += 0.1;
            this.alpha -= this.decay;
        }
        
        draw(ctx) {
            ctx.save();
            ctx.globalAlpha = this.alpha;
            ctx.fillStyle = `hsl(${this.hue}, 100%, 60%)`;
            ctx.beginPath();
            ctx.arc(this.x, this.y, 2, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }
    }
    
    const canvas = document.getElementById('fireworksCanvas');
    const ctx = canvas.getContext('2d');
    let fireworks = [];
    
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();
    
    function spawnFirework() {
        const startX = Math.random() * canvas.width;
        const startY = canvas.height;
        const targetX = Math.random() * canvas.width;
        const targetY = Math.random() * canvas.height * 0.5;
        fireworks.push(new Firework(startX, startY, targetX, targetY));
    }
    
    function animate() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        if (Math.random() < 0.03) {
            spawnFirework();
        }
        
        fireworks.forEach(fw => {
            fw.update();
            fw.draw(ctx);
        });
        
        fireworks = fireworks.filter(fw => !fw.exploded || fw.particles.length > 0);
        requestAnimationFrame(animate);
    }
    
    animate();
    
    window.celebrate = function(count = 5) {
        for (let i = 0; i < count; i++) {
            setTimeout(spawnFirework, i * 200);
        }
    };
    </script>
</body>
</html>
""", unsafe_allow_html=True)

# --- Title Section ---
st.markdown("""
<div class="container-fluid">
    <div class="row justify-content-center">
        <div class="col-12 text-center mb-4">
            <h1 class="display-1 title-glow mb-3">
                🎆 DIWALI ANONYMOUS MAILER 🎆
            </h1>
            <h2 class="text-warning mb-3">
                <i class="fas fa-sparkles"></i> Welcome to the Anonymous World <i class="fas fa-sparkles"></i>
            </h2>
            <p class="lead text-light">
                <i class="fas fa-diya-lamp"></i> Festival of Lights meets Futuristic Communication <i class="fas fa-diya-lamp"></i>
            </p>
            <p class="text-light">Experience the magic of Diwali while sending anonymous messages!</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sound toggle in sidebar
with st.sidebar:
    sound_enabled = st.checkbox("🔊 Enable Sound", value=st.session_state.sound_enabled)
    st.session_state.sound_enabled = sound_enabled

# --- Main App Logic ---
if not st.session_state.authenticated:
    # Authentication Form
    st.markdown("""
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card diwali-card">
                    <div class="card-body p-4">
                        <h3 class="card-title text-center text-warning mb-4">
                            <i class="fas fa-key"></i> Enter Your Access Code
                        </h3>
    """, unsafe_allow_html=True)
    
    with st.form(key='auth_form'):
        auth_code = st.text_input("", placeholder="e.g., ABC-123", key="auth_input").strip()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("🚀 Authenticate", use_container_width=True)

        if submit_button:
            play_keypress_sound()
            if st.session_state.auth_service.validate_and_use_code(auth_code):
                st.session_state.authenticated = True
                play_welcome_sound()
                
                st.markdown("""
                <script>
                setTimeout(() => {
                    if (typeof celebrate === 'function') {
                        celebrate(8);
                    }
                }, 500);
                </script>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="alert celebration-alert text-center">
                    <h2 class="text-success mb-3">
                        <i class="fas fa-party-horn"></i> WELCOME TO THE ANONYMOUS WORLD! <i class="fas fa-party-horn"></i>
                    </h2>
                    <p class="lead text-success">✨ Authentication Successful! The festival magic begins... ✨</p>
                    <div style="font-size: 3em;">🎆🎊🎆</div>
                </div>
                """, unsafe_allow_html=True)
                
                time.sleep(3)
                st.rerun()
            else:
                st.error("❌ Invalid or already used code. Please try again.")
    
    st.markdown("""
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # Email Composition Form
    st.markdown("""
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card diwali-card">
                    <div class="card-body p-4">
                        <h3 class="card-title text-center text-warning mb-4">
                            <i class="fas fa-envelope"></i> Compose Your Anonymous Email
                        </h3>
    """, unsafe_allow_html=True)
    
    with st.form(key='email_form'):
        recipient = st.text_input("📧 Recipient's Email", placeholder="john.doe@example.com").strip()
        subject = st.text_input("📝 Subject", placeholder="Your message subject").strip()
        content = st.text_area("💬 Message Content", height=200, placeholder="Write your anonymous message here...").strip()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("🚀 Launch Message into Digital Sky", use_container_width=True)

        if submit_button:
            play_keypress_sound()
            if not recipient or not subject or not content:
                st.warning("⚠️ Please fill in all fields to send your message.")
            else:
                try:
                    with st.spinner("🎆 Preparing your message for launch..."):
                        is_queued = st.session_state.email_service.queue_email_for_sending(recipient, subject, content)

                    if is_queued:
                        play_welcome_sound()
                        
                        st.markdown("""
                        <script>
                        setTimeout(() => {
                            if (typeof celebrate === 'function') {
                                celebrate(12);
                            }
                        }, 500);
                        </script>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("""
                        <div class="alert celebration-alert text-center">
                            <div style="font-size: 4em; margin: 20px 0;">🎆🚀🎆</div>
                            <h2 class="text-success mb-3">MESSAGE LAUNCHED INTO THE DIGITAL SKY!</h2>
                            <p class="lead text-success">✨ Your anonymous message has been queued successfully! ✨</p>
                            <p class="text-success">🪔 The Diwali magic will deliver it soon... 🪔</p>
                            <div style="font-size: 3em; margin: 20px 0;">🎊🎉🎊</div>
                        </div>
                        """, unsafe_allow_html=True)

                        time.sleep(4)
                        st.session_state.authenticated = False
                        st.rerun()
                    else:
                        st.error("🚫 Failed to queue email. It may contain inappropriate content. Please revise and try again.")
                except Exception as e:
                    st.error(f"❌ An error occurred while queuing the email: {e}")
    
    st.markdown("""
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div class="container-fluid mt-5">
    <div class="row">
        <div class="col-12 text-center">
            <hr style="border-color: rgba(255,255,255,0.3);">
            <div class="text-light p-3">
                <p><i class="fas fa-cog"></i> Use <code>python jobs/sender_job.py</code> to process queued emails in the background.</p>
                <p><i class="fas fa-fireworks"></i> Happy Diwali! May your messages bring joy and light! <i class="fas fa-fireworks"></i></p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)