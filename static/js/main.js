document.addEventListener('DOMContentLoaded', () => {
    console.log('JS loaded');
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
    }

    document.querySelectorAll('a[href^="/"]').forEach(link => {
        link.addEventListener('click', () => {
            if (navLinks) navLinks.classList.remove('active');
            if (navToggle) navToggle.classList.remove('active');
        });
    });

    // Scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature-card, .leaderboard-row, .stat-item').forEach(el => {
        if (!el.closest('#leaderboardTable')) {
            el.classList.add('scroll-animate');
            observer.observe(el);
        }
    });

    // Leaderboard client-side sorting
    try {
        const filterBtns = document.querySelectorAll('.filter-btn');
        const table = document.getElementById('leaderboardTable');
        if (filterBtns.length && table) {
            const rows = Array.from(table.querySelectorAll('.leaderboard-row')).filter(r => !r.classList.contains('header'));
            console.log('Found', rows.length, 'leaderboard rows');

            filterBtns.forEach(btn => {
                btn.addEventListener('click', () => {
                    filterBtns.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');

                    const sortBy = btn.dataset.sort;
                    const dir = btn.dataset.dir;

                    rows.sort((a, b) => {
                        let valA, valB;
                        if (sortBy === 'level') {
                            valA = parseInt(a.dataset.level) || 0;
                            valB = parseInt(b.dataset.level) || 0;
                        } else if (sortBy === 'total_xp') {
                            valA = parseInt(a.dataset.xp) || 0;
                            valB = parseInt(b.dataset.xp) || 0;
                        } else {
                            valA = parseInt(a.dataset.messages) || 0;
                            valB = parseInt(b.dataset.messages) || 0;
                        }
                        return dir === 'desc' ? valB - valA : valA - valB;
                    });

                    // Re-append sorted rows and update ranks
                    rows.forEach((row, idx) => {
                        const rankSpan = row.querySelector('.rank');
                        if (rankSpan) rankSpan.textContent = `#${idx + 1}`;
                        table.appendChild(row);
                    });
                });
            });
        }
    } catch (e) {
        console.error('Leaderboard error:', e);
    }
});
