window.addEventListener('load', function() {
    const princi = document.querySelector(".princi");
    const me5 = document.querySelector(".me-5");
  
    fetch('/check-auth/')
      .then(response => response.json())
      .then(data => {
        if (data.is_authenticated) {
          princi.style.display = "none";
          me5.style.display = "block";
        } else {
          princi.style.display = "block";
          me5.style.display = "none";
        }
      })
      .catch(error => {
        // Lidar com erros, se houver
        console.error('Erro ao verificar autenticação:', error);
      });
  });
  


  window.addEventListener('load', function() {
    const me5 = document.querySelector(".me-5");
    const mostrar = document.querySelector(".mostrar");

    me5.addEventListener('mouseover', function() {
        mostrar.style.display = "block";
    });

    mostrar.addEventListener('mouseover', function() {
        mostrar.style.display = "block";
    });

    mostrar.addEventListener('mouseout', function() {
        mostrar.style.display = "none";
    });
});