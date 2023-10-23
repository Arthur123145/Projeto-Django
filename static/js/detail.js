document.addEventListener('DOMContentLoaded', function() {
    const iconeCurtir = document.getElementById('icone-curtir');

    // Verifique o estado no localStorage e atualize o ícone, se necessário
    const isCurtido = localStorage.getItem('curtido');
    if (isCurtido === 'true') {
        iconeCurtir.classList.add('icone-curtir-vermelho');
    }

    iconeCurtir.addEventListener('click', function() {
        iconeCurtir.classList.toggle('icone-curtir-vermelho');

        // Armazene o estado no localStorage
        if (iconeCurtir.classList.contains('icone-curtir-vermelho')) {
            localStorage.setItem('curtido', 'true');
        } else {
            localStorage.setItem('curtido', 'false');
        }
    });

    iconeCurtir.addEventListener('mouseover', function() {
        iconeCurtir.style.cursor = 'pointer';
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const iconeComentar = document.getElementById('icone-comentar');
    const secaoComentario = document.querySelector('.comentario');

    iconeComentar.addEventListener('click', function() {
        if (secaoComentario.style.display === 'none' || secaoComentario.style.display === '') {
            secaoComentario.style.display = 'block';
        } else {
            secaoComentario.style.display = 'none';
        }
    });
});