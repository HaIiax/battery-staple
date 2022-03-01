document.addEventListener('DOMContentLoaded', () => {

    handleLinks('.time-link');
    handleLinks('.driver-link');

    function handleLinks(linkType) {

        // Get all "time-link" elements
        const $timeLinks = Array.prototype.slice.call(document.querySelectorAll(linkType), 0);

        // Check if there are any time-link elements
        if ($timeLinks.length > 0) {

            // Add a click event on each of them
            $timeLinks.forEach(el => {
                el.addEventListener('click', () => {

                    // Get the target from the "data-target" attribute
                    const targets = el.dataset.target;
                    targets.split("|").forEach(target => {
                        const $target = document.getElementById(target);

                        // Set myself active
                        if (!el.classList.contains('is-active')) {
                            el.classList.add('is-active')
                        }
                        // Set my target visible
                        if (!($target === null)) {
                            $target.classList.remove('is-hidden')
                        }

                        // Find the rest of the targets, make not active and hidden, or in the case of all, visible
                        $timeLinks.forEach(oth => {
                            const othTarget = oth.dataset.target;
                            const $othTarget = document.getElementById(othTarget);
                            if (othTarget != target) {
                                // Make the other time nav inactive
                                if (oth.classList.contains('is-active')) {
                                    oth.classList.remove('is-active')
                                }
                                // All - set all targets visible             
                                if (target == 'all') {
                                    if (!($othTarget === null)) {
                                        if ($othTarget.classList.contains('is-hidden')) {
                                            $othTarget.classList.remove('is-hidden')
                                        }
                                    }
                                } else {
                                    // Make the other target hidden
                                    if (!($othTarget === null)) {
                                        if (!$othTarget.classList.contains('is-hidden')) {
                                            $othTarget.classList.add('is-hidden')
                                        }
                                    }
                                }
                            }
                        }); // end of single target

                    }); // end of all targets

                });
            });
        }
    }

    // Get all "nav-link" elements
    const $navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav-link'), 0);

    // Check if there are any nav-link elements
    if ($navLinks.length > 0) {

        // Add a click event on each of them
        $navLinks.forEach(el => {
            el.addEventListener('click', () => {

                // Get the target from the "data-target" attribute
                const target = el.dataset.target;

                // Set myself active
                if (!el.classList.contains('is-active')) {
                    el.classList.add('is-active')
                }
                // Set my target(s) visible
                target.split('|').forEach(ctarget => {
                    const $ctarget = document.getElementById(ctarget);
                    if (!($ctarget === null)) {
                        $ctarget.classList.remove('is-hidden')
                    }
                })

                // Find the rest of the targets, make not active and hidden, or in the case of all, visible
                $navLinks.forEach(oth => {
                    const othTarget = oth.dataset.target;
                    if (othTarget != target) {
                        // Make the other time nav inactive
                        if (oth.classList.contains('is-active')) {
                            oth.classList.remove('is-active')
                        }
                        // Make the other target hidden
                        othTarget.split('|').forEach(ctarget => {
                            const $othTarget = document.getElementById(ctarget);
                            if (!($othTarget === null)) {
                                if (!$othTarget.classList.contains('is-hidden')) {
                                    $othTarget.classList.add('is-hidden')
                                }
                            }
                        })
                    }
                });

            });
        });
    }

});   