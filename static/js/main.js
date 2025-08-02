// Main JavaScript for TechMart

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            setTimeout(function() {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Add to cart animation
    const addToCartButtons = document.querySelectorAll('button[type="submit"]');
    addToCartButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const form = this.closest('form');
            if (form && form.action.includes('add_to_cart')) {
                // Add loading state
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Adding...';
                this.disabled = true;
                
                // Re-enable after a short delay (form will submit)
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.disabled = false;
                }, 2000);
            }
        });
    });

    // Quantity selector validation
    const quantitySelects = document.querySelectorAll('select[name="quantity"]');
    quantitySelects.forEach(function(select) {
        select.addEventListener('change', function() {
            const quantity = parseInt(this.value);
            const stockQuantity = parseInt(this.getAttribute('data-stock'));
            
            if (stockQuantity && quantity > stockQuantity) {
                alert(`Only ${stockQuantity} items available in stock.`);
                this.value = stockQuantity;
            }
        });
    });

    // Search functionality
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // Auto-submit search after 1 second of no typing
                if (this.value.length >= 3 || this.value.length === 0) {
                    this.closest('form').submit();
                }
            }, 1000);
        });
    }

    // Cart quantity update with AJAX-like behavior
    const cartQuantitySelects = document.querySelectorAll('.cart-item-card select[name="quantity"]');
    cartQuantitySelects.forEach(function(select) {
        select.addEventListener('change', function() {
            const form = this.closest('form');
            if (form) {
                // Add loading state to the row
                const cartItem = this.closest('.cart-item-card');
                cartItem.style.opacity = '0.6';
                cartItem.style.pointerEvents = 'none';
                
                // Submit the form
                form.submit();
            }
        });
    });

    // Image lazy loading fallback
    const images = document.querySelectorAll('img[src]');
    images.forEach(function(img) {
        img.addEventListener('error', function() {
            // Replace broken images with placeholder
            this.style.display = 'none';
            const placeholder = document.createElement('div');
            placeholder.className = 'placeholder-image';
            placeholder.innerHTML = '<i class="fas fa-image"></i>';
            this.parentNode.insertBefore(placeholder, this);
        });
    });

    // Product card hover effects
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let hasErrors = false;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    hasErrors = true;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (hasErrors) {
                e.preventDefault();
                // Scroll to first error
                const firstError = this.querySelector('.is-invalid');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
            }
        });
    });

    // Price formatting
    const priceElements = document.querySelectorAll('.price, .price-large');
    priceElements.forEach(function(element) {
        const price = parseFloat(element.textContent.replace('$', ''));
        if (!isNaN(price)) {
            element.textContent = '$' + price.toFixed(2);
        }
    });

    // Back to top button
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopButton.className = 'btn btn-primary position-fixed';
    backToTopButton.style.cssText = `
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: none;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    `;
    
    document.body.appendChild(backToTopButton);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });
    
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Dynamic content loading states
    const dynamicForms = document.querySelectorAll('form[method="POST"]');
    dynamicForms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                submitButton.disabled = true;
                
                // Fallback to re-enable after 10 seconds
                setTimeout(() => {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                }, 10000);
            }
        });
    });

    // Enhanced mobile menu
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking on links
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                if (window.innerWidth < 992) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                    bsCollapse.hide();
                }
            });
        });
    }

    // Console welcome message
    console.log('%cWelcome to TechMart! 🖥️', 'color: #0d6efd; font-size: 20px; font-weight: bold;');
    console.log('Built with Flask, Bootstrap, and lots of ❤️');
});

// Utility functions
window.TechMart = {
    // Format currency
    formatPrice: function(price) {
        return '$' + parseFloat(price).toFixed(2);
    },
    
    // Show notification
    showNotification: function(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.parentNode.removeChild(alertDiv);
            }
        }, 5000);
    },
    
    // Confirm action
    confirmAction: function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    }
};
