/* ═══════════════════════════════════════════════════
   DP Control Panel — Optimized Particle System
   Neon Effects - No Freezing
   ═══════════════════════════════════════════════════ */

(function () {
  const canvas = document.getElementById('particleCanvas');
  if (!canvas) return;

  // Background ambient canvas stays behind UI
  const ctx = canvas.getContext('2d');

  // Click & Touch Ripple Burst Canvas
  // Positioned as a non-blocking top overlay at z-index: 950 above the UI cards
  // with pointer-events: none and touch-action: none so mobile clicks and typing pass through instantly!
  let clickCanvas = document.getElementById('clickEffectCanvas');
  if (!clickCanvas) {
    clickCanvas = document.createElement('canvas');
    clickCanvas.id = 'clickEffectCanvas';
    document.body.appendChild(clickCanvas);
  }
  Object.assign(clickCanvas.style, {
    position: 'fixed',
    top: '0',
    left: '0',
    width: '100vw',
    height: '100vh',
    zIndex: '950',
    pointerEvents: 'none',
    touchAction: 'none'
  });
  clickCanvas.setAttribute('aria-hidden', 'true');
  const clickCtx = clickCanvas.getContext('2d');

  let particles = [];
  let clickParticles = [];
  let width = 0;
  let height = 0;

  const MAX_PARTICLES = 80;
  const MAX_CLICK_EFFECTS = 120;
  const CONNECTION_DISTANCE = 140;
  const PRIMARY_RGB = '79, 140, 255';
  const CYAN_RGB = '34, 211, 238';
  const PURPLE_RGB = '168, 85, 247';
  const PINK_RGB = '236, 72, 153';
  const YELLOW_RGB = '251, 191, 36';
  const ORANGE_RGB = '249, 115, 22';
  const MAGENTA_RGB = '217, 70, 239';
  const GREEN_RGB = '52, 211, 153';
  const EMERALD_RGB = '16, 185, 129';
  const AMBER_RGB = '245, 158, 11';
  const RED_RGB = '244, 63, 94';

  let mouse = { x: null, y: null, active: false };

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    clickCanvas.width = width;
    clickCanvas.height = height;
  }

  window.addEventListener('resize', resize);
  resize();

  window.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
    mouse.active = true;
  });

  window.addEventListener('mouseleave', () => {
    mouse.active = false;
  });

  // Tap & Click Trigger - Non-blocking top overlay with intelligent Enable vs Disable action awareness.
  // Debounces synthetic clicks on mobile so taps trigger only once.
  let lastTouchTime = 0;

  function getEffectTypeFromTarget(target) {
    if (!target) return null;
    const el = target.closest ? target.closest('.btn-action-enable, .btn-action-disable, .toggle-active-btn, .toggle-btn, .feature-card-toggle, [data-effect]') : null;
    if (!el) return null;
    if (el.dataset && el.dataset.effect) return el.dataset.effect;
    if (el.classList.contains('btn-action-enable')) return 'enable';
    if (el.classList.contains('btn-action-disable')) return 'disable';
    if (el.classList.contains('toggle-active-btn') || el.classList.contains('toggle-btn')) {
      const text = (el.textContent || '').trim().toLowerCase();
      if (text.includes('enable')) return 'enable';
      if (text.includes('disable')) return 'disable';
    }
    if (el.classList.contains('feature-card-toggle')) {
      return el.classList.contains('checked') ? 'disable' : 'enable';
    }
    return null;
  }

  window.addEventListener('touchstart', (e) => {
    if (e.touches && e.touches.length > 0) {
      lastTouchTime = Date.now();
      const touch = e.touches[0];
      const type = getEffectTypeFromTarget(e.target);
      createNeonClick(touch.clientX, touch.clientY, type);
    }
  }, { passive: true });

  window.addEventListener('click', (e) => {
    if (Date.now() - lastTouchTime < 450) return;
    const type = getEffectTypeFromTarget(e.target);
    createNeonClick(e.clientX, e.clientY, type);
  }, { passive: true });

  // Background Particle - Slow & Elegant
  class Particle {
    constructor() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * 0.25;
      this.vy = (Math.random() - 0.5) * 0.25 + 0.03;
      this.radius = Math.random() * 2.5 + 1;
      this.alpha = Math.random() * 0.4 + 0.15;
      this.color = [PRIMARY_RGB, CYAN_RGB, PURPLE_RGB][Math.floor(Math.random() * 3)];
      this.pulse = Math.random() * Math.PI * 2;
      this.isTwinkle = Math.random() > 0.82;
      this.twinkleRotation = Math.random() * Math.PI;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.pulse += 0.008;
      this.twinkleRotation += 0.006;

      if (this.x < -10) this.x = width + 10;
      if (this.x > width + 10) this.x = -10;
      if (this.y > height + 20) {
        this.y = -20;
        this.x = Math.random() * width;
      }
    }

    draw() {
      const glow = Math.sin(this.pulse) * 0.3 + 0.5;

      // Triple glow layers
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius * 3, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${this.color}, ${this.alpha * glow * 0.1})`;
      ctx.fill();

      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius * 1.8, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${this.color}, ${this.alpha * glow * 0.15})`;
      ctx.fill();

      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${this.color}, ${this.alpha})`;
      ctx.fill();

      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius * 0.3, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, ${this.alpha * 0.5})`;
      ctx.fill();

      // Constellation stars
      if (this.isTwinkle) {
        const arm = this.radius * (2.8 + glow);
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.twinkleRotation);
        ctx.beginPath();
        ctx.moveTo(0, -arm);
        ctx.lineTo(this.radius * 0.3, -this.radius * 0.3);
        ctx.lineTo(arm, 0);
        ctx.lineTo(this.radius * 0.3, this.radius * 0.3);
        ctx.lineTo(0, arm);
        ctx.lineTo(-this.radius * 0.3, this.radius * 0.3);
        ctx.lineTo(-arm, 0);
        ctx.lineTo(-this.radius * 0.3, -this.radius * 0.3);
        ctx.closePath();
        ctx.fillStyle = `rgba(255, 255, 255, ${this.alpha * glow * 0.72})`;
        ctx.fill();
        ctx.restore();
      }
    }
  }

  // Neon Click Particle - Rainbow or Action-themed Colors
  class NeonClick {
    constructor(x, y, palette) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 1.5 + Math.random() * 2.5;

      this.x = x;
      this.y = y;
      this.previousX = x;
      this.previousY = y;
      this.vx = Math.cos(angle) * speed;
      this.vy = Math.sin(angle) * speed - 0.3;
      this.size = Math.random() * 2.4 + 1.35;
      this.life = 1;
      this.decay = 0.014 + Math.random() * 0.004;
      this.rotation = Math.random() * Math.PI;
      this.spin = (Math.random() - 0.5) * 0.12;
      this.isStar = Math.random() > 0.42;
      const colors = (palette && palette.length) ? palette : [CYAN_RGB, PRIMARY_RGB, PURPLE_RGB, PINK_RGB, YELLOW_RGB, ORANGE_RGB, MAGENTA_RGB];
      this.color = colors[Math.floor(Math.random() * colors.length)];
    }

    update() {
      this.previousX = this.x;
      this.previousY = this.y;
      this.x += this.vx;
      this.y += this.vy;
      this.vy += 0.1;
      this.vx *= 0.97;
      this.rotation += this.spin;
      this.life -= this.decay;
      return this.life > 0;
    }

    draw() {
      const alpha = this.life;

      // Trail
      const trail = clickCtx.createLinearGradient(this.previousX, this.previousY, this.x, this.y);
      trail.addColorStop(0, `rgba(${this.color}, 0)`);
      trail.addColorStop(1, `rgba(${this.color}, ${alpha * 0.9})`);
      clickCtx.beginPath();
      clickCtx.moveTo(this.previousX - this.vx * 3.5, this.previousY - this.vy * 3.5);
      clickCtx.lineTo(this.x, this.y);
      clickCtx.strokeStyle = trail;
      clickCtx.lineWidth = Math.max(0.7, this.size * 0.62);
      clickCtx.stroke();

      // Soft colored halo
      clickCtx.beginPath();
      clickCtx.arc(this.x, this.y, this.size * 5, 0, Math.PI * 2);
      clickCtx.fillStyle = `rgba(${this.color}, ${alpha * 0.35})`;
      clickCtx.fill();

      // Bright neon core
      clickCtx.beginPath();
      clickCtx.arc(this.x, this.y, this.size * 1.5, 0, Math.PI * 2);
      clickCtx.fillStyle = `rgba(${this.color}, ${alpha})`;
      clickCtx.fill();

      // Four-point twinkle
      if (this.isStar) {
        const arm = this.size * 2.35;
        clickCtx.save();
        clickCtx.translate(this.x, this.y);
        clickCtx.rotate(this.rotation);
        clickCtx.beginPath();
        clickCtx.moveTo(0, -arm);
        clickCtx.lineTo(this.size * 0.42, -this.size * 0.42);
        clickCtx.lineTo(arm, 0);
        clickCtx.lineTo(this.size * 0.42, this.size * 0.42);
        clickCtx.lineTo(0, arm);
        clickCtx.lineTo(-this.size * 0.42, this.size * 0.42);
        clickCtx.lineTo(-arm, 0);
        clickCtx.lineTo(-this.size * 0.42, -this.size * 0.42);
        clickCtx.closePath();
        clickCtx.fillStyle = `rgba(255, 255, 255, ${alpha * 0.95})`;
        clickCtx.fill();
        clickCtx.restore();
      }

      // White impact point
      clickCtx.beginPath();
      clickCtx.arc(this.x, this.y, this.size * 0.6, 0, Math.PI * 2);
      clickCtx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
      clickCtx.fill();
    }
  }

  // Create neon click effect - Rainbow Colors & Expanding Water Ripples
  // Enhanced with support for 'enable' (emerald-green) and 'disable' (amber-warning) themes
  function createNeonClick(x, y, effectType) {
    const incomingEffectCount = 31;
    const maximumExisting = MAX_CLICK_EFFECTS - incomingEffectCount;
    if (clickParticles.length > maximumExisting) {
      clickParticles.splice(0, clickParticles.length - maximumExisting);
    }

    let sparkColors;
    let ringColors;
    let rayColors;
    let bloomCore;
    let bloomMid;

    if (effectType === 'enable') {
      sparkColors = [GREEN_RGB, EMERALD_RGB, CYAN_RGB, '110, 231, 183', '167, 243, 208'];
      ringColors = [GREEN_RGB, CYAN_RGB, EMERALD_RGB];
      rayColors = [GREEN_RGB, CYAN_RGB, EMERALD_RGB, '167, 243, 208'];
      bloomCore = GREEN_RGB;
      bloomMid = CYAN_RGB;
    } else if (effectType === 'disable') {
      sparkColors = [AMBER_RGB, YELLOW_RGB, ORANGE_RGB, RED_RGB, '253, 230, 138'];
      ringColors = [AMBER_RGB, ORANGE_RGB, RED_RGB];
      rayColors = [AMBER_RGB, YELLOW_RGB, ORANGE_RGB, RED_RGB];
      bloomCore = AMBER_RGB;
      bloomMid = RED_RGB;
    } else {
      sparkColors = [CYAN_RGB, PRIMARY_RGB, PURPLE_RGB, PINK_RGB, YELLOW_RGB, ORANGE_RGB, MAGENTA_RGB];
      ringColors = [CYAN_RGB, PURPLE_RGB, PINK_RGB];
      rayColors = [CYAN_RGB, PRIMARY_RGB, PURPLE_RGB, PINK_RGB, MAGENTA_RGB];
      bloomCore = CYAN_RGB;
      bloomMid = PURPLE_RGB;
    }

    for (let i = 0; i < 20; i++) {
      clickParticles.push(new NeonClick(x, y, sparkColors));
    }

    // Expanding water-ripple rings with rich color shifts
    for (let r = 0; r < 3; r++) {
      clickParticles.push({
        x: x,
        y: y,
        r: r,
        radius: 0,
        life: 1,
        delay: r * 0.085,
        color: ringColors[r % ringColors.length],
        update: function() {
          if (this.delay > 0) {
            this.delay -= 0.02;
            return true;
          }
          this.radius += 2.55;
          this.life -= 0.02;
          return this.life > 0;
        },
        draw: function() {
          if (this.delay > 0) return;
          if (this.radius <= 0) return;

          const a = this.life;

          // Diffuse outside glow
          clickCtx.beginPath();
          clickCtx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
          clickCtx.strokeStyle = `rgba(${this.color}, ${a * 0.42})`;
          clickCtx.lineWidth = 15;
          clickCtx.stroke();

          // Saturated water edge
          clickCtx.beginPath();
          clickCtx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
          clickCtx.strokeStyle = `rgba(${this.color}, ${a})`;
          clickCtx.lineWidth = 3.2;
          clickCtx.stroke();

          // Fine white crest
          clickCtx.beginPath();
          clickCtx.arc(this.x, this.y, this.radius - 1, 0, Math.PI * 2);
          clickCtx.strokeStyle = `rgba(255, 255, 255, ${a * 0.92})`;
          clickCtx.lineWidth = 1.15;
          clickCtx.stroke();
        }
      });
    }

    // Seven radial light rays create a crisp supernova moment behind the rings
    for (let ray = 0; ray < 7; ray++) {
      const angle = Math.random() * Math.PI * 2;
      const length = 38 + Math.random() * 42;
      const color = rayColors[ray % rayColors.length];
      clickParticles.push({
        x: x,
        y: y,
        angle: angle,
        length: length,
        color: color,
        life: 1,
        update: function() {
          this.life -= 0.018;
          return this.life > 0;
        },
        draw: function() {
          const progress = 1 - this.life;
          const start = this.length * Math.max(0, progress - 0.13);
          const end = this.length * Math.min(1, progress + 0.2);
          const x1 = this.x + Math.cos(this.angle) * start;
          const y1 = this.y + Math.sin(this.angle) * start;
          const x2 = this.x + Math.cos(this.angle) * end;
          const y2 = this.y + Math.sin(this.angle) * end;
          const gradient = clickCtx.createLinearGradient(x1, y1, x2, y2);
          gradient.addColorStop(0, `rgba(255, 255, 255, ${this.life * 0.95})`);
          gradient.addColorStop(0.42, `rgba(${this.color}, ${this.life * 0.88})`);
          gradient.addColorStop(1, `rgba(${this.color}, 0)`);
          clickCtx.beginPath();
          clickCtx.moveTo(x1, y1);
          clickCtx.lineTo(x2, y2);
          clickCtx.strokeStyle = gradient;
          clickCtx.lineWidth = 2.5;
          clickCtx.stroke();
        }
      });
    }

    // Luminous impact bloom
    clickParticles.push({
      x: x,
      y: y,
      life: 0.62,
      update: function() {
        this.life -= 0.055;
        return this.life > 0;
      },
      draw: function() {
        const radius = 68 * this.life;
        const bloom = clickCtx.createRadialGradient(this.x, this.y, 0, this.x, this.y, radius);
        bloom.addColorStop(0, `rgba(255, 255, 255, ${this.life * 0.9})`);
        bloom.addColorStop(0.18, `rgba(${bloomCore}, ${this.life * 0.65})`);
        bloom.addColorStop(0.52, `rgba(${bloomMid}, ${this.life * 0.22})`);
        bloom.addColorStop(1, 'rgba(0, 0, 0, 0)');
        clickCtx.beginPath();
        clickCtx.arc(this.x, this.y, radius, 0, Math.PI * 2);
        clickCtx.fillStyle = bloom;
        clickCtx.fill();
      }
    });
  }

  // Draw connections
  function drawConnections() {
    for (let i = 0; i < particles.length; i++) {
      const p1 = particles[i];

      for (let j = i + 1; j < Math.min(i + 15, particles.length); j++) {
        const p2 = particles[j];
        const dx = p1.x - p2.x;
        const dy = p1.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < CONNECTION_DISTANCE) {
          const alpha = (1 - dist / CONNECTION_DISTANCE) * 0.12;
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          const line = ctx.createLinearGradient(p1.x, p1.y, p2.x, p2.y);
          line.addColorStop(0, `rgba(${p1.color}, ${alpha})`);
          line.addColorStop(1, `rgba(${p2.color}, ${alpha * 0.68})`);
          ctx.strokeStyle = line;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }

      if (mouse.active) {
        const dx = p1.x - mouse.x;
        const dy = p1.y - mouse.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < CONNECTION_DISTANCE * 1.2) {
          const alpha = (1 - dist / (CONNECTION_DISTANCE * 1.2)) * 0.2;
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.strokeStyle = `rgba(${CYAN_RGB}, ${alpha})`;
          ctx.lineWidth = 1.2;
          ctx.stroke();
        }
      }
    }
  }

  // Initialize
  for (let i = 0; i < MAX_PARTICLES; i++) {
    particles.push(new Particle());
  }

  // Animation loop
  function animate() {
    ctx.clearRect(0, 0, width, height);
    clickCtx.clearRect(0, 0, width, height);

    particles.forEach(p => {
      p.update();
      p.draw();
    });

    drawConnections();

    clickParticles = clickParticles.filter(p => p.update());

    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    clickCtx.save();
    clickParticles.forEach(p => p.draw());
    clickCtx.restore();
    ctx.restore();

    requestAnimationFrame(animate);
  }

  // Global manual trigger helper
  window.triggerNeonClick = function(x, y, type) {
    createNeonClick(x, y, type);
  };

  animate();
})();
