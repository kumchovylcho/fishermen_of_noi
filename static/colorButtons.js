document.addEventListener("DOMContentLoaded", function() {
            const currentUrl = window.location.href;
            console.log(currentUrl)
            const links = document.querySelectorAll("nav ul li a");
            links.forEach(function(link) {
                if (link.href === currentUrl) {
                    link.classList.add("active");
                }
            });
        });
