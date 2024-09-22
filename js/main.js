// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Dynamic navigation menu
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            
            // Check if we're on the index page
            const isIndexPage = window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/');

            if (href === '#' || href === 'index.html' || href === '../index.html') {
                if (isIndexPage) {
                    // If on index page, scroll to top
                    e.preventDefault();
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                } else {
                    // If not on index page, allow default behavior (navigate to home)
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
        });
    });

    // Contact form validation and submission
    const contactForm = document.getElementById('contact-form');

    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const name = contactForm.querySelector('#name').value.trim();
            const email = contactForm.querySelector('#email').value.trim();
            const message = contactForm.querySelector('#message').value.trim();
            
            if (name && email && message) {
                // Here you would typically send the form data to a server
                console.log('Form submitted:', { name, email, message });
                alert('Thank you for your message! I\'ll get back to you soon.');
                contactForm.reset();
            } else {
                alert('Please fill in all fields.');
            }
        });
    }

    // Add a simple animation to section headers
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