# X-Serv-CSS-Elaborado
Django cms_css elaborado

## Enunciado

Modifica tu solución para "Django cms_put" de forma que:

* Si el recurso está bajo "/css/", se almacene tal cual al recibirlo (mediante PUT) y se sirva tal cual (cuando se recibe un GET).
* Si el recurso tiene cualquier otro nombre, se almacene de tal forma cuando se reciba (mediante PUT) que el contenido almacenado sea el cuerpo (lo que va en el elemento BODY) de las páginas que se sirvan (cuando se reciba el GET correspondiente). Para servir las páginas utiliza una plantilla (template) que incluya el uso de la hoja de estilo "/css/main.css" para manejar la apariencia de todas las páginas.
