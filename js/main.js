document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector(".hamburger");
    const navMenu = document.querySelector(".nav-menu");

    hamburger.addEventListener("click", () => {
        hamburger.classList.toggle("active");
        navMenu.classList.toggle("active");
    })

    document.querySelectorAll(".nav-menu li a").forEach(n => n.addEventListener("click", () => {
        hamburger.classList.remove("active");
        navMenu.classList.remove("active");
    }))

    // Existing smooth scrolling functionality
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            
            const isIndexPage = window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/');

            if (href === '#' || href === 'index.html' || href === '../index.html') {
                if (isIndexPage) {
                    e.preventDefault();
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                } else {
                    return;
                }
            } else if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                const targetSection = document.getElementById(targetId);
                if (targetSection) {
                    targetSection.scrollIntoView({ behavior: 'smooth' });
                }
            }

            // Close menu after clicking a link (for mobile)
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
        });
    });

    // Contact form validation and submission
    const contactForm = document.getElementById('contact-form');

    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const name = contactForm.querySelector('#name').value.trim();
            const email = contactForm.querySelector('#email').value.trim();
            const subject = contactForm.querySelector('#subject').value.trim();
            const message = contactForm.querySelector('#message').value.trim();
            
            if (name && email && subject && message) {
                // Construct the mailto link
                const mailtoLink = `mailto:info@marvinmtz.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(`Name: ${name}\nEmail: ${email}\n\n${message}`)}`;
                
                // Open the user's default email client
                window.location.href = mailtoLink;

                alert('Thank you for your message! Your default email client should open with a pre-filled email. Please send the email to complete your message submission.');
                contactForm.reset();
            } else {
                alert('Please fill in all fields.');
            }
        });
    }

    // Section header animation
    const sectionHeaders = document.querySelectorAll('section > h2');

    sectionHeaders.forEach(header => {
        header.style.opacity = '0';
        header.style.transition = 'opacity 0.5s ease-in-out';

        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                    }, 300);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        observer.observe(header);
    });
});