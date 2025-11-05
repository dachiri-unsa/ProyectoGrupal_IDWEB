  const botonesComprar = document.querySelectorAll('.btn-comprar');
  const listaCarrito = document.getElementById('lista-carrito');
  const total = document.getElementById('total');
  const carrito = document.getElementById('carrito');
  const btnCarrito = document.getElementById('btn-carrito');
  const vaciarBtn = document.getElementById('vaciar-carrito');

  let carritoItems = [];

  // Mostrar/ocultar carrito
  btnCarrito.addEventListener('click', () => {
    carrito.classList.toggle('oculto');
  });

  // Añadir producto
  botonesComprar.forEach(boton => {
    boton.addEventListener('click', () => {
      const nombre = boton.getAttribute('data-nombre');
      const precio = parseFloat(boton.getAttribute('data-precio'));

      const productoExistente = carritoItems.find(item => item.nombre === nombre);

      if (productoExistente) {
        productoExistente.cantidad++;
      } else {
        carritoItems.push({ nombre, precio, cantidad: 1 });
      }

      actualizarCarrito();
    });
  });

  // Vaciar carrito
  vaciarBtn.addEventListener('click', () => {
    carritoItems = [];
    actualizarCarrito();
  });

  // Actualizar carrito visual
  function actualizarCarrito() {
    listaCarrito.innerHTML = '';
    let totalPagar = 0;

    carritoItems.forEach(item => {
      const li = document.createElement('li');
      li.textContent = `${item.nombre} x${item.cantidad}`;
      const span = document.createElement('span');
      span.textContent = `S/${(item.precio * item.cantidad).toFixed(2)}`;
      li.appendChild(span);
      listaCarrito.appendChild(li);

      totalPagar += item.precio * item.cantidad;
    });

    total.textContent = `Total: S/${totalPagar.toFixed(2)}`;
  }