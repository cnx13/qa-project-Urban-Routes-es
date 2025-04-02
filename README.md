# Automatización de Pruebas de Urban Routes

Christian Apodaca. Proyecto Sprint 8.

## Descripción del Proyecto

Este proyecto automatiza las pruebas de la aplicación web Urban Routes utilizando Selenium WebDriver. Cubre varias funcionalidades, incluyendo la configuración de rutas, la solicitud de un taxi, la adición de una tarjeta de pago, la introducción de un número de teléfono y la adición de solicitudes especiales para el viaje.

## Tecnologías y Técnicas

-   **Python:** El lenguaje de programación principal utilizado para escribir los scripts de las pruebas.
-   **Selenium WebDriver:** Utilizado para automatizar las interacciones del navegador web.
-   **Chrome WebDriver:** Utilizado específicamente para controlar el navegador Chrome.
-   **pytest:** Un marco de pruebas para escribir y ejecutar pruebas.
-   **Selectores XPath y CSS:** Utilizados para localizar elementos web.
-   **WebDriverWait y Condiciones Esperadas:** Utilizados para manejar elementos web dinámicos y asegurar que los elementos sean interactivos antes de las acciones.
-   **Modelo de Objetos de Página (Page Object Model):** La clase `UrbanRoutesPage` representa la página web y encapsula sus elementos y acciones.
-   **Registro (Rendimiento):** Utilizado para recuperar el código SMS de los registros de red.

## Archivos

-   **`main.py`:** Contiene los scripts de prueba y la clase `UrbanRoutesPage`.
-   **`data.py`:** Contiene datos de prueba como URLs, direcciones, números de teléfono y detalles de la tarjeta.

## Configuración

1.  **Instalar Python:** Asegúrate de tener Python 3.6 o posterior instalado.
2.  **Instalar Dependencias:** Ejecuta el siguiente comando para instalar los paquetes de Python requeridos:

    ```bash
    pip install selenium pytest
    ```

3.  **Descargar ChromeDriver:** Descarga el ejecutable de ChromeDriver que coincida con la versión de tu navegador Chrome y colócalo en un directorio incluido en el PATH de tu sistema.

## Instalación y Uso de Librerías

-   **Selenium:**
    -      Instalación: `pip install selenium`
    -      Uso: Importa las clases y funciones necesarias desde el módulo `selenium`, como `webdriver`, `By`, `WebDriverWait`, y `expected_conditions`.
-   **pytest:**
    -      Instalación: `pip install pytest`
    -      Uso: Escribe funciones de prueba que comiencen con `test_` y ejecuta `pytest` en la terminal para descubrir y ejecutar las pruebas.

## Ejecutar las Pruebas en la Terminal

1.  **Navegar al Directorio del Proyecto:** Abre tu terminal y navega al directorio que contiene `main.py` y `data.py`.
2.  **Ejecutar pytest:** Ejecuta el siguiente comando para ejecutar las pruebas:

    ```bash
    pytest main.py -v -s
    ```

    -   `-v` (verbose) proporciona una salida detallada.
    -   `-s` deshabilita la captura de salida, permitiendo que se muestren las declaraciones de impresión.

## Casos de Prueba

El archivo `main.py` incluye los siguientes casos de prueba:

-   `test_set_route`: Prueba la configuración de las direcciones "desde" y "hasta".
-   `test_request_taxi`: Prueba la solicitud de un taxi y la selección de la opción "Comfort".
-   `test_phone_number`: Prueba la introducción de un número de teléfono y la verificación del código SMS.
-   `test_add_card`: Prueba la adición de una tarjeta de pago.
-   `test_message_driver`: Prueba la introducción de un mensaje para el conductor.
-   `test_add_blanket`: Prueba la funcionalidad de agregar una solicitud de manta/pañuelos.
-   `test_add_icecream`: Prueba la funcionalidad de agregar una solicitud de helado.
-   `test_request_ride_confirmation`: Prueba la funcionalidad de confirmar la solicitud del viaje.

## Notas Importantes

-   La función `retrieve_phone_code` se utiliza para extraer el código de verificación SMS de los registros de red. Esta función solo debe llamarse después de que la aplicación haya solicitado el código.
-   Asegúrate de que la versión de ChromeDriver coincida con la versión de tu navegador Chrome para evitar problemas de compatibilidad.
-   Las pruebas asumen que la aplicación web se está ejecutando en la URL especificada en `data.py`.
-   Los XPaths utilizados en el código son muy específicos, si la interfaz de usuario de la aplicación cambia, los XPaths deberán actualizarse.