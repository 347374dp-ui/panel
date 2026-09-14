/* ═══════════════════════════════════════════════════
   DP Control Panel — Optimized Particle System
   Neon Effects - No Freezing
   ═══════════════════════════════════════════════════ */

(function () {
  const canvas = document.getElementById('particleCanvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
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

  let mouse = { x: null, y: null, active: false };

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
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

  window.addEventListener('click', (e) => {
    const interactive = e.target.closest('a, button, input, select, textarea, label, [role="button"], .exporter-tab');
    if (interactive) return;
    createNeonClick(e.clientX, e.clientY);
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
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.pulse += 0.008;

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
    }
  }

  // Neon Click Particle - Rainbow Colors
  class NeonClick {
    constructor(x, y) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 1.5 + Math.random() * 2;

      this.x = x;
      this.y = y;
      this.vx = Math.cos(angle) * speed;
      this.vy = Math.sin(angle) * speed - 0.3;
      this.size = Math.random() * 2.4 + 1.35;
      this.life = 1;
      this.decay = 0.027 + Math.random() * 0.009;
      this.rotation = Math.random() * Math.PI;
      this.spin = (Math.random() - 0.5) * 0.12;
      this.isStar = Math.random() > 0.42;
      const colors = [PRIMARY_RGB, CYAN_RGB, PURPLE_RGB, PINK_RGB, YELLOW_RGB, ORANGE_RGB, MAGENTA_RGB];
      this.color = colors[Math.floor(Math.random() * colors.length)];
    }

    update() {
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

      // Soft colored halo
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size * 5, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${this.color}, ${alpha * 0.18})`;
      ctx.fill();

      // Bright neon core
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size * 1.5, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${this.color}, ${alpha})`;
      ctx.fill();

      // Four-point twinkle, modeled after the supplied sparkle reference.
      if (this.isStar) {
        const arm = this.size * 2.35;
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        ctx.beginPath();
        ctx.moveTo(0, -arm);
        ctx.lineTo(this.size * 0.42, -this.size * 0.42);
        ctx.lineTo(arm, 0);
        ctx.lineTo(this.size * 0.42, this.size * 0.42);
        ctx.lineTo(0, arm);
        ctx.lineTo(-this.size * 0.42, this.size * 0.42);
        ctx.lineTo(-arm, 0);
        ctx.lineTo(-this.size * 0.42, -this.size * 0.42);
        ctx.closePath();
        ctx.fillStyle = `rgba(255, 255, 255, ${alpha * 0.88})`;
        ctx.fill();
        ctx.restore();
      }

      // White impact point
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size * 0.6, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
      ctx.fill();
    }
  }

  // Create neon click effect - Rainbow Colors
  function createNeonClick(x, y) {
    // Reserve room for the entire new burst before adding it. This keeps rapid
    // clicks smooth instead of allowing several overlapping bursts to build up.
    const incomingEffectCount = 23;
    const maximumExisting = MAX_CLICK_EFFECTS - incomingEffectCount;
    if (clickParticles.length > maximumExisting) {
      clickParticles.splice(0, clickParticles.length - maximumExisting);
    }

    // A compact burst feels richer than a huge amount of heavy particles.
    for (let i = 0; i < 20; i++) {
      clickParticles.push(new NeonClick(x, y));
    }

    // Expanding water-ripple rings with slight colour shifts.
    const ringColors = [CYAN_RGB, PURPLE_RGB, PINK_RGB];
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
          this.life -= 0.025;
          return this.life > 0;
        },
        draw: function() {
          if (this.delay > 0) return;
          if (this.radius <= 0) return;

          const a = this.life;

          // Diffuse outside glow
          ctx.beginPath();
          ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
          ctx.strokeStyle = `rgba(${this.color}, ${a * 0.24})`;
          ctx.lineWidth = 12;
          ctx.stroke();

          // Saturated water edge
          ctx.beginPath();
          ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
          ctx.strokeStyle = `rgba(${this.color}, ${a * 0.92})`;
          ctx.lineWidth = 2.7;
          ctx.stroke();

          // Fine white crest
          ctx.beginPath();
          ctx.arc(this.x, this.y, this.radius - 1, 0, Math.PI * 2);
          ctx.strokeStyle = `rgba(255, 255, 255, ${a * 0.78})`;
          ctx.lineWidth = 0.9;
          ctx.stroke();
        }
      });
    }

    // Luminous impact bloom, kept short so the page never flashes heavily.
    clickParticles.push({
      x: x,
      y: y,
      life: 0.62,
      update: function() {
        this.life -= 0.055;
        return this.life > 0;
      },
      draw: function() {
        const radius = 44 * this.life;
        const bloom = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, radius);
        bloom.addColorStop(0, `rgba(255, 255, 255, ${this.life * 0.9})`);
        bloom.addColorStop(0.18, `rgba(${CYAN_RGB}, ${this.life * 0.65})`);
        bloom.addColorStop(0.52, `rgba(${PURPLE_RGB}, ${this.life * 0.22})`);
        bloom.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.beginPath();
        ctx.arc(this.x, this.y, radius, 0, Math.PI * 2);
        ctx.fillStyle = bloom;
        ctx.fill();
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
          ctx.strokeStyle = `rgba(${PRIMARY_RGB}, ${alpha})`;
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

    particles.forEach(p => {
      p.update();
      p.draw();
    });

    drawConnections();

    clickParticles = clickParticles.filter(p => p.update());
    clickParticles.forEach(p => p.draw());

    requestAnimationFrame(animate);
  }

  animate();
})();
