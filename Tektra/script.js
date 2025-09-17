// Tektra Website JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initNavigation();
    initScrollEffects();
    initContactForm();
    initLoginModal();
    initSignupModal();
    initAnimations();
});

// Navigation functionality
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    // Smooth scrolling for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 70; // Account for fixed navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
                
                // Update active link
                navLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });
    
    // Mobile menu toggle
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking on a link
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
            }
        });
    });
}

// Scroll effects
function initScrollEffects() {
    const navbar = document.querySelector('.navbar');
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Navbar background on scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(10, 10, 15, 0.95)';
            navbar.style.backdropFilter = 'blur(20px)';
        } else {
            navbar.style.background = 'rgba(10, 10, 15, 0.8)';
            navbar.style.backdropFilter = 'blur(20px)';
        }
    });
    
    // Active section highlighting
    window.addEventListener('scroll', function() {
        let current = '';
        const scrollPosition = window.scrollY + 100;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

// Contact form functionality
function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const name = formData.get('name');
            const email = formData.get('email');
            const message = formData.get('message');
            
            // Simple validation
            if (!name || !email || !message) {
                showNotification('Please fill in all fields.', 'error');
                return;
            }
            
            if (!isValidEmail(email)) {
                showNotification('Please enter a valid email address.', 'error');
                return;
            }
            
            // Simulate form submission
            showNotification('Message sent! We\'ll get back to you soon.', 'success');
            this.reset();
        });
    }
}

// Login modal functionality
function initLoginModal() {
    const loginModal = document.getElementById('loginModal');
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            if (!username || !password) {
                showNotification('Please fill in all fields.', 'error');
                return;
            }
            
            // Simulate login
            showNotification('Login successful!', 'success');
            setTimeout(() => {
                closeLoginModal();
            }, 1500);
        });
    }
}

// Signup modal functionality
function initSignupModal() {
    const signupForm = document.getElementById('signupForm');
    
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('signup-name').value;
            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;
            const confirmPassword = document.getElementById('signup-confirm').value;
            const terms = document.getElementById('terms').checked;
            
            if (!name || !email || !password || !confirmPassword) {
                showNotification('Please fill in all fields.', 'error');
                return;
            }
            
            if (!isValidEmail(email)) {
                showNotification('Please enter a valid email address.', 'error');
                return;
            }
            
            if (password !== confirmPassword) {
                showNotification('Passwords do not match.', 'error');
                return;
            }
            
            if (!terms) {
                showNotification('Please agree to the Terms of Service.', 'error');
                return;
            }
            
            // Simulate signup
            showNotification('Account created successfully!', 'success');
            setTimeout(() => {
                closeSignupModal();
            }, 1500);
        });
    }
}

// Animation effects
function initAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animatedElements = document.querySelectorAll('.feature-card, .gallery-item, .stat, .contact-item');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
    
    // Floating cards animation
    const floatingCards = document.querySelectorAll('.card');
    floatingCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 2}s`;
    });
}

// Utility functions
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        const offsetTop = section.offsetTop - 70;
        window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }
}

function openLoginModal() {
    const modal = document.getElementById('loginModal');
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
}

function closeLoginModal() {
    const modal = document.getElementById('loginModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

function openSignupModal() {
    const modal = document.getElementById('signupModal');
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
}

function closeSignupModal() {
    const modal = document.getElementById('signupModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        z-index: 3000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    `;
    
    // Set background color based on type
    switch (type) {
        case 'success':
            notification.style.background = 'linear-gradient(135deg, #10B981, #059669)';
            break;
        case 'error':
            notification.style.background = 'linear-gradient(135deg, #EF4444, #DC2626)';
            break;
        case 'warning':
            notification.style.background = 'linear-gradient(135deg, #F59E0B, #D97706)';
            break;
        default:
            notification.style.background = 'linear-gradient(135deg, #3B82F6, #2563EB)';
    }
    
    // Add to DOM
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 5000);
}

// Close modal when clicking outside
window.addEventListener('click', function(e) {
    const modal = document.getElementById('loginModal');
    if (e.target === modal) {
        closeLoginModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeLoginModal();
    }
});

// Parallax effect for hero background
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const stars = document.querySelector('.stars');
    const mountains = document.querySelector('.mountains');
    
    if (stars) {
        stars.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
    
    if (mountains) {
        mountains.style.transform = `translateY(${scrolled * 0.3}px)`;
    }
});

// Add loading animation
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
});

// Add CSS for loading animation
const style = document.createElement('style');
style.textContent = `
    body {
        opacity: 0;
        transition: opacity 0.5s ease;
    }
    
    body.loaded {
        opacity: 1;
    }
    
    .nav-menu.active {
        display: flex;
        flex-direction: column;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: rgba(10, 10, 15, 0.95);
        backdrop-filter: blur(20px);
        padding: 20px;
        border-top: 1px solid rgba(244, 114, 182, 0.1);
    }
    
    .hamburger.active span:nth-child(1) {
        transform: rotate(45deg) translate(5px, 5px);
    }
    
    .hamburger.active span:nth-child(2) {
        opacity: 0;
    }
    
    .hamburger.active span:nth-child(3) {
        transform: rotate(-45deg) translate(7px, -6px);
    }
    
    @media (max-width: 768px) {
        .nav-menu {
            display: none;
        }
    }
`;
document.head.appendChild(style);
