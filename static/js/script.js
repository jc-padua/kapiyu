let image = document.querySelector('#image');

image.addEventListener('mouseover', function () {
    image.style.borderRadius = '50%';
})
image.addEventListener('mouseout', function () {
    image.style.borderRadius = '0%';
})