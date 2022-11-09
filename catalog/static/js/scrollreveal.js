elementsReveal();

function elementsReveal() {
    window.sr = ScrollReveal({ reset: true });

    sr.reveal('.header-animation', { 
        origin: 'top', 
        duration: 1500,
        distance : '30px',
        easing: 'ease',
        reset: false, 
    });
    sr.reveal('.logo__circle', { 
        origin: 'left', 
        duration: 1000,
        distance : '30px',
        easing: 'ease',
    });
    sr.reveal('.logo__title', { 
        origin: 'right', 
        duration: 1500,
        distance : '30px',
        easing: 'ease',
    });
    sr.reveal('.movies__carousel', { 
        origin: 'right', 
        duration: 1500,
        distance : '200px',
        easing: 'ease',
    });
    // sr.reveal('.schedule__day', { 
    //     origin: 'left',
    //     duration: 1500,
    //     distance : '50px',
    //     easing: 'ease',
    //     reset: false,
    // });
    sr.reveal('.auth-error', { 
        origin: 'top',
        duration: 1000,
        distance : '10px',
        easing: 'ease',
        reset: false,
    });
    sr.reveal('.ticket', { 
        origin: 'left',
        duration: 1000,
        distance : '100px',
        easing: 'ease',
        reset: false,
    });
    sr.reveal('.movies-list', { 
        origin: 'bottom',
        duration: 1000,
        distance : '100px',
        easing: 'ease',
        reset: false,
    });
    sr.reveal('#left', { 
        origin: 'left',
        duration: 1000,
        distance : '20px',
        easing: 'ease',
        reset: false,
    });
    sr.reveal('#right', { 
        origin: 'right',
        duration: 1000,
        distance : '20px',
        easing: 'ease',
        reset: false,
    });
    sr.reveal('.about__left', { 
        origin: 'left',
        duration: 1000,
        distance : '20px',
        easing: 'ease',
        reset: false,
    });
    sr.reveal('.about__right', { 
        origin: 'right',
        duration: 1000,
        distance : '20px',
        easing: 'ease',
        reset: false,
    });
    sr.reveal('.about__title', { 
        origin: 'top',
        duration: 1000,
        distance : '20px',
        easing: 'ease',
        reset: false,
    });
}