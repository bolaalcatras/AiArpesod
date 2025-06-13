# Análisis del Repositorio: https://github.com/julianxitoso/InventarioTI

## Archivo: `repo_temporal/buscar.php`

```markdown
## Resumen de `repo_temporal/buscar.php`

**Propósito Principal:**

El archivo `buscar.php` proporciona una interfaz para buscar activos tecnológicos en una base de datos, filtrando por cédula del responsable, regional, empresa y estado (incluyendo o excluyendo los dados de baja).  Los resultados se muestran agrupados por responsable.  Permite la exportación de los resultados a un archivo Excel.

**Descripción de Funciones y Clases:**

*   **No hay clases definidas.**
*   **Funciones:**
    *   `getEstadoBadgeClass($estado)`:  Retorna la clase CSS de Bootstrap para un badge (etiqueta visual) según el estado del activo.  Permite mostrar visualmente el estado del activo (asignado, en mantenimiento, dado de baja, etc.).

**Lógica Principal:**

1.  **Autenticación y Autorización:**
    *   Requiere autenticación previa del usuario mediante `backend/auth_check.php`.
    *   Restringe el acceso a la página a usuarios con roles 'admin', 'tecnico', 'auditor' o 'registrador'.
2.  **Conexión a la Base de Datos:**
    *   Establece una conexión a la base de datos utilizando `backend/db.php`.
    *   Maneja errores de conexión.
    *   Define el charset a utf8mb4 para soportar caracteres especiales.
3.  **Recuperación de Datos de Sesión y Parámetros de Búsqueda:**
    *   Obtiene el nombre y rol del usuario actual de la sesión.
    *   Recupera los parámetros de búsqueda de la URL (cédula, regional, empresa, incluir dados de baja, buscar todos).
4.  **Construcción y Ejecución de la Consulta SQL:**
    *   Construye una consulta SQL dinámicamente, basada en los parámetros de búsqueda.
    *   Utiliza prepared statements para prevenir inyecciones SQL.
    *   Realiza la búsqueda en la tabla `activos_tecnologicos`, uniendo con las tablas `usuarios`, `tipos_activo` y `cargos` para obtener información relacionada al responsable y al tipo de activo.
    *   Se agregan filtros por cédula, regional y empresa si se proporcionan.
    *   Incluye o excluye los activos dados de baja según la selección del usuario.
    *   Ordena los resultados por nombre, cédula del usuario y ID del activo.
5.  **Presentación de Resultados:**
    *   Muestra un formulario de búsqueda.
    *   Si hay un error en la consulta, muestra un mensaje de error.
    *   Si la búsqueda es exitosa, muestra los activos encontrados, agrupados por responsable.
    *   Para cada activo, muestra información relevante como tipo, marca, serie, estado, valor, fecha de registro y enlaces para ver el historial y editar (si el usuario tiene los permisos necesarios).
    *   El estado del activo se muestra con un badge de Bootstrap cuyo color depende del estado.
    *   Ofrece la opción de exportar los resultados a Excel.
    *   Si no se encuentran activos, muestra un mensaje indicando que no hay resultados.
6.  **Cerrado de la Conexión:**
    *   Cierra la conexión a la base de datos.

**Dependencias Clave:**

*   `backend/auth_check.php`:  Gestiona la autenticación y autorización de usuarios.
*   `backend/db.php`:  Establece la conexión a la base de datos.
*   `logout.php`: Permite cerrar la sesión del usuario.
*   `exportar_excel.php`: Permite exportar los resultados de la búsqueda a un archivo Excel.
*   Funciones `tiene_permiso_para()`: (Asumida) Determina si el usuario actual tiene permisos para realizar ciertas acciones, como editar activos o generar informes.
*   Bootstrap (CSS y JS): Para el diseño y la interfaz de usuario.
*   Bootstrap Icons: Para los iconos de la interfaz.
```

---

## Archivo: `repo_temporal/buscar_datos_usuario.php`

```markdown
## Resumen del archivo `repo_temporal/buscar_datos_usuario.php`

**Propósito Principal:**

El archivo `buscar_datos_usuario.php` tiene como objetivo principal buscar y devolver información de un usuario a partir de su cédula (identificación).  Retorna un objeto JSON conteniendo los detalles del usuario si se encuentra, o un mensaje indicando que no se encontró o si hubo un error.

**Descripción de Funciones/Clases:**

El archivo no define clases ni funciones personalizadas, sino que implementa lógica directamente en el script. Las principales acciones son:

1.  **Validación de la conexión a la base de datos:** Verifica si existe una conexión válida y, si no, devuelve un error.
2.  **Obtención del parámetro de cédula:** Recupera el valor de la cédula desde el parámetro `GET` y lo limpia.
3.  **Consulta a la base de datos:** Realiza una consulta SQL a la tabla `usuarios` (con un `LEFT JOIN` a la tabla `cargos`) para buscar los datos del usuario por su cédula.
4.  **Construcción de la respuesta JSON:** Crea un array `$response` con los datos del usuario o mensajes de error. Luego, codifica este array en formato JSON y lo envía como respuesta.
5.  **Manejo de errores:** Utiliza `error_log` para registrar errores en el log del servidor.
6.  **Cierre de la conexión:** Cierra la conexión a la base de datos después de la consulta.

**Cambios Principales Destacados:**

*   **Consulta JOIN:** La consulta SQL ahora incluye un `LEFT JOIN` con la tabla `cargos` para obtener el nombre del cargo del usuario. Esto significa que el cargo ya no se busca en la tabla `usuarios` directamente, sino que se obtiene de la tabla `cargos`.
*   **Eliminación de fallback:** Se ha eliminado la lógica que buscaba información en la tabla `activos_tecnologicos` si no se encontraba en la tabla `usuarios`. Ahora, la tabla `usuarios` es la única fuente de información para los datos del usuario.

**Dependencias Clave:**

*   **`backend/auth_check.php`:**  Se asume que este archivo realiza algún tipo de comprobación de autenticación o autorización.
*   **`backend/db.php`:** Este archivo es crucial porque establece y proporciona la conexión a la base de datos (`$conn` o `$conexion`). Utiliza esta conexión para realizar las consultas.
*   **`$_GET['cedula']`:**  Es la cédula del usuario que se busca, enviada como parámetro en la URL.
*   **MySQL (a través de la extensión mysqli):** El script interactúa directamente con una base de datos MySQL.
```

---

## Archivo: `repo_temporal/cambiar_clave.php`

```markdown
## Resumen del archivo `repo_temporal/cambiar_clave.php`

**Propósito principal:**

Este archivo permite a los usuarios autenticados cambiar su contraseña dentro de la aplicación.  Incluye validaciones del lado del servidor para asegurar que la nueva contraseña cumpla con ciertos criterios (longitud mínima, confirmación correcta) y que la contraseña actual ingresada sea correcta. También incluye la interfaz de usuario para el formulario de cambio de contraseña.

**Descripción de las funciones y clases:**

El archivo no define clases ni funciones explícitas.  Su lógica principal se encuentra directamente en el script PHP, que incluye:

*   **Autenticación:** Verifica si el usuario ha iniciado sesión mediante la comprobación de la variable de sesión `$_SESSION["loggedin"]`. Si no ha iniciado sesión, lo redirige a la página de inicio de sesión (`login.php`).
*   **Conexión a la base de datos:** Incluye el archivo `backend/db.php` para establecer una conexión a la base de datos.  Verifica si la conexión se estableció correctamente.
*   **Obtención de datos del usuario:** Recupera la información del usuario (nombre completo, rol y cédula) de la sesión para mostrarla en la barra superior y utilizarla en la consulta de actualización de contraseña.
*   **Validación de la entrada del usuario:**  Valida que todos los campos del formulario se hayan completado y que la nueva contraseña y su confirmación coincidan. Verifica también que la longitud de la nueva contraseña sea suficiente.
*   **Verificación de la contraseña actual:** Consulta la base de datos para obtener el hash de la contraseña actual del usuario y lo compara con la contraseña actual ingresada por el usuario utilizando `password_verify()`.
*   **Actualización de la contraseña:** Si la contraseña actual es correcta, genera un nuevo hash para la nueva contraseña utilizando `password_hash()` y actualiza la contraseña en la base de datos.
*   **Manejo de errores:** Muestra mensajes de error y éxito al usuario, y registra los errores en el registro del servidor mediante `error_log()`.
*   **Interfaz de usuario (HTML):**  Genera el formulario para que el usuario ingrese su contraseña actual, la nueva contraseña y la confirmación de la nueva contraseña. Utiliza Bootstrap para el diseño. Incluye JavaScript para la validación en tiempo real de la confirmación de la nueva contraseña.
*   **Barra superior:** Muestra información del usuario (nombre, rol) y un botón de cierre de sesión.

**Dependencias clave:**

*   **`backend/auth_check.php`:**  Gestiona la autenticación del usuario y las variables de sesión relacionadas con el inicio de sesión.
*   **`backend/db.php`:**  Establece la conexión a la base de datos.
*   **`$_SESSION`:** Utilizada para almacenar y recuperar información sobre la sesión del usuario (estado de inicio de sesión, nombre de usuario, rol, etc.).
*   **`password_hash()` y `password_verify()`:**  Funciones de PHP para generar y verificar hashes de contraseñas de forma segura.
*   **Bootstrap (CSS y JavaScript):**  Utilizado para el diseño y la interactividad del formulario.
*   **Bootstrap Icons:** Utilizados para iconos.

**Consideraciones Importantes:**

*   **Seguridad:** El script utiliza `password_hash()` y `password_verify()` para almacenar las contraseñas de forma segura.  Es importante asegurarse de que la configuración del servidor sea compatible con los algoritmos utilizados por estas funciones.
*   **Validación:** El script realiza validaciones tanto en el lado del servidor (PHP) como en el lado del cliente (JavaScript).  La validación del lado del servidor es fundamental para la seguridad y la integridad de los datos.
*   **Manejo de errores:** El script registra los errores en el registro del servidor para facilitar la depuración.  También muestra mensajes de error amigables al usuario.
*   **Columnas de la base de datos:** El código asume que las columnas de la base de datos para el nombre de usuario y la contraseña son 'usuario' y 'clave', respectivamente. **ES CRUCIAL** verificar y ajustar estas columnas según la estructura real de la base de datos. El código contiene comentarios indicando esto.
*   **Cierre de conexión:** El comentario indica que la conexión no se cierra explícitamente porque podría ser usada por otras partes del sistema.  Se debe tener cuidado con esto para evitar problemas de conexión.
```

---

## Archivo: `repo_temporal/centro_gestion.php`

```markdown
## Resumen de `repo_temporal/centro_gestion.php`

**Propósito Principal:**

El archivo `centro_gestion.php` representa el panel de control o "centro de gestión" de una aplicación web de inventario TI.  Ofrece una interfaz centralizada con enlaces a diferentes módulos de administración, tales como gestión de usuarios, activos, roles, cargos, proveedores y préstamos. El acceso está restringido a usuarios con roles específicos (por defecto, 'admin').

**Descripción:**

El script realiza las siguientes acciones:

1.  **Inicia la sesión:**  `session_start()`  permite el uso de variables de sesión.
2.  **Verifica la autenticación y autorización:** Incluye el archivo `backend/auth_check.php` para autenticar al usuario y luego utiliza la función `restringir_acceso_pagina(['admin'])` para limitar el acceso a usuarios con el rol 'admin' (o roles definidos).
3.  **Obtiene información del usuario de la sesión:**  Recupera el nombre completo y el rol del usuario actual de las variables de sesión (`$_SESSION['nombre_usuario_completo']` y `$_SESSION['rol_usuario']`). Si estas variables no están definidas, se establecen valores predeterminados ('Administrador' y 'admin', respectivamente).
4.  **Construye la interfaz de usuario (HTML):**
    *   **Barra de navegación superior:** Muestra el logo, el nombre del usuario actual y su rol, y un botón para cerrar sesión.
    *   **Título de la página:**  "Centro de Gestión".
    *   **Panel de control (Management Hub):**  Muestra una cuadrícula de tarjetas, cada una de las cuales representa un módulo de administración diferente.  Cada tarjeta tiene un icono, un título y una breve descripción. Las tarjetas son enlaces a otros scripts PHP (por ejemplo, `gestionar_usuarios.php`, `gestionar_activos.php`, `gestionar_roles.php`, etc.).
    *   **Footer:**  Muestra información del desarrollador y enlaces a redes sociales.
5.  **Estilo:** Define estilos CSS en la sección `<head>` para la apariencia de la página, utilizando principalmente Bootstrap para la estructura y diseño.

**Funciones/Clases:**

*   No hay clases definidas directamente en este archivo.  Sin embargo, se basa en la función `restringir_acceso_pagina` definida en el archivo `backend/auth_check.php`.

**Dependencias Clave:**

*   **`backend/auth_check.php`:**  Este archivo es crucial para la seguridad, ya que es responsable de la autenticación y autorización de los usuarios. Contiene la función `restringir_acceso_pagina`.
*   **`logout.php`:** Maneja el cierre de sesión del usuario.
*   **Variables de sesión (`$_SESSION`)**: El script depende de las variables de sesión para obtener la información del usuario y el rol.
*   **Bootstrap (CSS y JS):**  La interfaz de usuario depende en gran medida de Bootstrap para el diseño y la funcionalidad.  Se utilizan tanto la hoja de estilo CSS como el JavaScript de Bootstrap.
*   **Bootstrap Icons:** Utiliza la biblioteca de iconos de Bootstrap para mostrar iconos representativos en las tarjetas del panel de control.
*   **Varios scripts de gestión (gestionar_usuarios.php, gestionar_activos.php, etc.):** Estos archivos manejan la lógica y la interfaz para cada uno de los módulos de administración a los que se accede desde el panel de control.
```

---

## Archivo: `repo_temporal/dashboard.php`

```markdown
## Resumen de `repo_temporal/dashboard.php`

### Propósito Principal
El archivo `dashboard.php` tiene como propósito principal proporcionar una vista general del inventario de activos tecnológicos, mostrando KPIs (Key Performance Indicators) y gráficos que resumen el estado, distribución y valor de dichos activos. Permite filtrar la información mostrada por regional, empresa o tipo de activo. Además, gestiona la autenticación del usuario, requiriendo una sesión activa para acceder al dashboard.

### Descripción de Funciones y Clases
El archivo no define clases, pero sí incluye las siguientes funciones:

*   **`ejecutarConsultaConFiltro($conexion_db, $sql_base_select_from_joins, $main_where_condition, $additional_where_conditions_str, $params_filtro, $types_filtro, $group_order_suffix = "")`**: Esta función es la encargada de ejecutar consultas SQL a la base de datos, permitiendo aplicar filtros dinámicos a la consulta.  Recibe la conexión a la base de datos, la parte inicial de la consulta SQL, la condición `WHERE` principal, condiciones `WHERE` adicionales, los parámetros para los filtros, los tipos de datos de los parámetros y un sufijo para las cláusulas `GROUP BY` y `ORDER BY`.  Prepara la consulta, realiza el `bind_param` (si hay parámetros) y ejecuta la consulta, devolviendo el resultado. También registra errores en el registro de errores del servidor.

Además, el código realiza las siguientes acciones principales:

1.  **Autenticación:** Verifica si existe una sesión de usuario activa. Si no, redirige a la página de login.
2.  **Autorización:** Mediante `auth_check.php` restringe el acceso a la página a usuarios con roles específicos (admin, técnico, auditor).
3.  **Conexión a la Base de Datos:** Establece una conexión a la base de datos MySQL. Si la conexión falla, muestra un mensaje de error. Intenta reutilizar una conexión existente (`$conn`), y si no está definida, crea una nueva usando credenciales hardcodeadas.  Esto representa un posible riesgo de seguridad y malas prácticas.
4.  **Obtención de Datos de la Sesión:** Recupera el nombre y rol del usuario actual desde la sesión.
5.  **Filtrado:** Obtiene los valores de los filtros (regional, empresa, tipo de activo) a partir de los parámetros GET.
6.  **Construcción de Consultas:** Construye dinámicamente las consultas SQL para obtener los datos necesarios para los KPIs y gráficos, aplicando los filtros seleccionados por el usuario. Utiliza la función `ejecutarConsultaConFiltro` para ejecutar las consultas.
7.  **Cálculo de KPIs:** Calcula los KPIs principales, como el total de activos, el valor total del inventario y el total de usuarios con activos.
8.  **Preparación de Datos para Gráficos:** Prepara los datos para los gráficos que muestran la distribución de activos por tipo, regional y empresa.
9.  **Respuesta AJAX:** Si la petición es AJAX, devuelve los datos en formato JSON para actualizar la interfaz de usuario de forma dinámica. Si no, muestra la página completa con los datos cargados.
10. **Presentación:** Construye el HTML para mostrar el dashboard, incluyendo los KPIs y gráficos. Utiliza Bootstrap para el diseño y Chart.js para los gráficos.

### Dependencias Clave
*   **`session_start()`:**  Para la gestión de sesiones de usuario.
*   **`login.php`:** Para redireccionar si no hay sesión activa.
*   **`backend/auth_check.php`:** Para verificar los permisos del usuario. La función `restringir_acceso_pagina()` es utilizada para limitar el acceso a ciertos roles.
*   **`backend/db.php`:** Para la conexión a la base de datos (aunque también tiene un fallback con credenciales hardcodeadas dentro del mismo archivo).
*   **MySQLi:** Para interactuar con la base de datos MySQL.
*   **Bootstrap:** Para el diseño de la página.
*   **Chart.js:** Para la generación de gráficos.
```

---

## Archivo: `repo_temporal/depreciacion_activos.php`

```markdown
## Resumen de `depreciacion_activos.php`

### Propósito Principal:

Este archivo PHP permite a usuarios con roles específicos (administrador, auditor, registrador, técnico) consultar la depreciación de activos tecnológicos.  Permite buscar activos por número de serie o por cédula del responsable, y luego muestra los detalles del activo, incluyendo el cálculo de la depreciación (anual, mensual, acumulada) y el valor en libros actual.  Si el activo no cumple con los requisitos para ser depreciado (según umbral UVT) o no tiene los datos necesarios (fecha de compra, valor, vida útil), se muestra un mensaje informativo.

### Descripción de Funciones y Clases:

*   **`get_asset_details_by_id($id, $conn)`**: Esta función recupera los detalles de un activo tecnológico de la base de datos, basándose en su ID.  Realiza una consulta SQL para obtener información del activo, el responsable, el cargo del responsable y el tipo de activo, uniendo tablas relevantes.  Retorna un array asociativo con la información del activo o `null` en caso de error o si no se encuentra el activo.

### Variables Globales Importantes:

*   `$conexion`:  Conexión a la base de datos (inyectada desde un `require_once`).
*   `VALOR_UVT_2025`:  Constante que define el valor de la UVT para el año 2025.
*   `UMBRAL_UVT_DEPRECIACION`: Constante que define el umbral en UVT a partir del cual un activo es depreciable.
*   `$nombre_usuario_actual_sesion`: El nombre del usuario actual obtenido de la sesión.
*   `$rol_usuario_actual_sesion`: El rol del usuario actual obtenido de la sesión.
*   `$activo_info_display`: Almacena los detalles del activo a mostrar, obtenidos de la base de datos.
*   `$depreciacion_info`: Almacena información relacionada con el cálculo de la depreciación del activo.
*   `$error_busqueda`: Almacena mensajes de error relacionados con la búsqueda de activos.
*   `$criterio_busqueda_val`: Almacena el criterio de búsqueda introducido por el usuario.
*   `$tipo_criterio_val`: Almacena el tipo de criterio de búsqueda seleccionado por el usuario (serie o cédula).
*   `$activos_del_responsable_lista`: Almacena una lista de activos asociados a un responsable, cuando la búsqueda se realiza por cédula.
*   `$nombre_responsable_buscado`: Almacena el nombre del responsable cuando la búsqueda se realiza por cédula.

### Lógica Principal:

1.  **Autenticación y Autorización:** Se verifica que el usuario tenga una sesión activa y un rol autorizado para acceder a la página mediante `auth_check.php`.
2.  **Conexión a la Base de Datos:** Se establece una conexión a la base de datos, manejando posibles errores de conexión.
3.  **Procesamiento de Búsqueda (POST):**
    *   Si se recibe una solicitud POST con el parámetro `buscar_activo_dep`, se obtiene el criterio y tipo de criterio de búsqueda.
    *   Se realiza una consulta a la base de datos según el tipo de criterio (serie o cédula).
    *   Si se encuentra el activo (por serie) o activos (por cédula), se almacena la información en las variables correspondientes.  En caso de búsqueda por cédula, se recupera una lista de activos.
    *   Se manejan errores de búsqueda, como criterios vacíos o activos no encontrados.
4.  **Visualización de Depreciación (GET):**
    *   Si se recibe una solicitud GET con la acción `ver_depreciacion` y el ID del activo, se consulta la base de datos para obtener los detalles del activo usando `get_asset_details_by_id`.
5.  **Cálculo de Depreciación:**
    *   Si se encontró un activo y tiene los datos necesarios (fecha de compra, valor aproximado, vida útil), se calcula la depreciación anual, mensual y acumulada, así como el valor en libros.
    *   Se considera el valor de la UVT y el umbral para determinar si el activo es depreciable.
    *   Se calcula la depreciación utilizando el método de línea recta.
6.  **Presentación:**
    *   Se muestra un formulario de búsqueda.
    *   Se muestran mensajes de error si los hay.
    *   Se muestra la información del activo y el cálculo de la depreciación en una tabla.
    *   Se utiliza HTML y CSS para la presentación visual.
    *   Se incorporan íconos de Bootstrap Icons para mejorar la interfaz.
    *   Se usa Bootstrap para la estructura de la página.

### Dependencias Clave:

*   **`backend/auth_check.php`**:  Gestiona la autenticación y autorización del usuario.
*   **`backend/db.php`**:  Establece la conexión a la base de datos.
*   **Bootstrap (CSS y JS)**:  Framework CSS para el diseño y la maquetación de la interfaz de usuario.
*   **Bootstrap Icons**: Biblioteca de iconos para la interfaz de usuario.
```

---

## Archivo: `repo_temporal/editar.php`

```markdown
## Resumen del archivo `repo_temporal/editar.php`

### Propósito Principal:

El archivo `editar.php` permite la administración de activos tecnológicos en un sistema.  Los usuarios con roles de 'admin' o 'tecnico' pueden buscar, editar, trasladar o dar de baja activos, así como eliminarlos físicamente (solo si no tienen historial).  Proporciona una interfaz para visualizar y modificar información detallada sobre los activos, así como realizar traslados masivos entre usuarios.

### Descripción de Funciones y Clases:

El archivo no define clases, pero contiene la siguiente funcionalidad principal:

1.  **Autenticación y Autorización:** Verifica el acceso del usuario mediante `auth_check.php` y restringe el acceso a roles específicos (`admin`, `tecnico`).

2.  **Conexión a la Base de Datos:** Establece una conexión a la base de datos utilizando `backend/db.php`.  Maneja errores de conexión críticos.

3.  **Definición de Constantes:** Define constantes para tipos de historial (actualización, traslado, baja, eliminación física).

4.  **Manejo de Sesión:** Utiliza variables de sesión para obtener información del usuario actual y para mensajes flash (mensajes de estado mostrados una sola vez).

5.  **Búsqueda de Activos:** Permite la búsqueda de activos por cédula del responsable, regional, empresa, o incluyendo los dados de baja.  Construye consultas SQL dinámicamente basadas en los criterios de búsqueda.

6.  **Edición de Activos:** Permite la modificación de los detalles de un activo, incluyendo tipo, marca, serie, estado, valor, fecha de compra, y otros detalles específicos.  Valida campos obligatorios.

7.  **Traslado Masivo de Activos:** Permite trasladar múltiples activos a un nuevo responsable.  Actualiza la información del responsable en la tabla `usuarios` y la asignación de activos en la tabla `activos_tecnologicos`.  Registra un evento de historial para cada traslado.

8.  **Dar de Baja Activos:** Permite marcar un activo como "Dado de Baja", estableciendo un motivo y observaciones.

9.  **Eliminación Física de Activos:** Permite la eliminación completa de un activo de la base de datos, pero solo si no tiene historial asociado.

10. **Funciones Helper:**
    - `input_editable()`:  Genera un campo de texto (input) en HTML para la edición de un atributo de un activo.  Puede ser configurado como de sólo lectura o editable.
    - `select_editable()`: Genera un campo de selección (select) en HTML con opciones predefinidas para la edición de un atributo de un activo.  Puede ser configurado como deshabilitado o editable.
    - `textarea_editable()`: Genera un campo de texto multilínea (textarea) en HTML para la edición de un atributo de un activo. Puede ser configurado como de sólo lectura o editable.

11. **Interfaz de Usuario:** Presenta una interfaz basada en Bootstrap para la búsqueda, visualización y edición de activos.

### Dependencias Clave:

*   `backend/auth_check.php`:  Gestiona la autenticación y autorización de usuarios.
*   `backend/db.php`:  Contiene la lógica para la conexión a la base de datos.
*   `backend/historial_helper.php`:  Proporciona funciones para registrar eventos en el historial de activos.
*   `buscar_datos_usuario.php`: (Mencionado indirectamente en el script)  Este archivo se encarga de buscar datos de usuarios basado en su cédula, usado en el proceso de traslado de activos.
*   Librerías de terceros: Bootstrap (CSS y JS), Bootstrap Icons.

En resumen, `editar.php` es un componente central para la gestión de activos tecnológicos, que abarca desde la búsqueda y edición individual hasta el traslado masivo y la eliminación (bajo ciertas condiciones), con un fuerte enfoque en la seguridad (autenticación, autorización) y la integridad de los datos (historial).
```

---

## Archivo: `repo_temporal/exportar_excel.php`

```markdown
## Resumen de `repo_temporal/exportar_excel.php`

**Propósito principal del archivo:**

El archivo `exportar_excel.php` genera informes en formato Excel (XLS) basados en datos de activos tecnológicos almacenados en una base de datos.  Permite a los usuarios (admin, tecnico, auditor) exportar información sobre activos, filtrada por diferentes criterios y rangos de fechas, para su análisis y gestión.

**Descripción de sus funciones/clases:**

El archivo no define clases ni funciones explícitas más allá del código PHP principal. La lógica se centra en:

1.  **Autenticación y Autorización:**  Verifica la sesión del usuario y restringe el acceso según el rol (admin, técnico, auditor).
2.  **Conexión a la Base de Datos:** Establece una conexión a la base de datos MySQL mediante `db.php`.  Gestiona errores de conexión.
3.  **Obtención y Validación de Parámetros:** Recibe el tipo de informe (`tipo_informe`), la fecha de inicio (`fecha_desde`) y la fecha de fin (`fecha_hasta`) como parámetros GET. Define valores predeterminados si no se proporcionan.
4.  **Construcción Dinámica de Consultas SQL:**  Construye consultas SQL dinámicamente en función del `tipo_informe` seleccionado.  Define constantes para tipos de eventos del historial. Implementa la lógica para agregar condiciones de filtro de fecha (fecha_compra para activos y fecha_evento para historial).
5.  **Preparación y Ejecución de Consultas:** Prepara las consultas SQL utilizando sentencias preparadas para prevenir inyecciones SQL. Vincula parámetros de forma segura.
6.  **Generación del Archivo Excel:**  Establece las cabeceras HTTP necesarias para forzar la descarga del contenido como un archivo Excel.  Genera el contenido de la tabla HTML que representa el informe.  Incluye el BOM (Byte Order Mark) para garantizar la correcta visualización de caracteres UTF-8 en Excel.
7.  **Manejo de Datos y Formato:** Itera sobre los resultados de la consulta, formatea los datos (por ejemplo, fechas y valores numéricos) y los inserta en las celdas de la tabla HTML. Implementa lógica especial para el informe de mantenimientos, que incluye datos JSON almacenados en la base de datos.
8.  **Manejo de Errores:** Incluye registros de error (`error_log`) para depurar problemas de conexión a la base de datos, preparación de consultas o ejecución de consultas.  Muestra mensajes de error amigables al usuario en caso de fallas.
9.  **Cierre de Conexión:** Cierra la conexión a la base de datos al finalizar.
10. **Definición de Constantes:** Define constantes para los tipos de eventos de historial si aún no están definidas, asegurando la disponibilidad de estas constantes.

**Dependencias clave:**

*   **`backend/auth_check.php`:**  Gestiona la autenticación y autorización de usuarios.  Contiene la función `restringir_acceso_pagina()` que verifica la sesión y restringe el acceso a usuarios no autorizados.
*   **`backend/db.php`:**  Establece la conexión a la base de datos MySQL.  Debe definir la variable `$conn` o `$conexion` con el objeto de conexión PDO o mysqli.
*   **`$_GET['tipo_informe']`:** Define el tipo de informe a generar.
*   **`$_GET['fecha_desde']` y `$_GET['fecha_hasta']`:** Definen el rango de fechas para filtrar los datos.

**Tablas de la base de datos referenciadas:**

*   `activos_tecnologicos`
*   `tipos_activo`
*   `usuarios`
*   `cargos`
*   `historial_activos`
```

---

## Archivo: `repo_temporal/generar_acta_devolucion_pdf.php`

```markdown
## Resumen del archivo `repo_temporal/generar_acta_devolucion_pdf.php`

**Propósito principal:**

Este archivo PHP genera un acta de devolución en formato PDF para un activo tecnológico que ha sido previamente prestado y ahora es devuelto. El acta contiene información detallada sobre el activo, los usuarios involucrados (quien devuelve y quien recibe) y las condiciones de la devolución.

**Descripción de funciones y clases:**

*   **`to_iso_devolucion($string)`:** Función que convierte una cadena de texto de UTF-8 a ISO-8859-1. Esto es necesario para asegurar la correcta visualización de caracteres especiales en el PDF generado con la librería FPDF, especialmente si se usan fuentes estándar.

*   **`PDF_Acta_Devolucion` (clase):**  Extiende la clase `FPDF` de la librería FPDF para personalizar la creación del PDF del acta de devolución. Incluye los siguientes métodos:
    *   `Header()`: Define el encabezado del PDF, incluyendo el logo de la empresa y el título del acta. Si el logo no se encuentra, registra un error en el log.
    *   `Footer()`: Define el pie de página del PDF, incluyendo el texto "Generado por Sistema de Inventario TI" y el número de página.
    *   `InfoCell($label, $value, $labelWidth = 55, $valueWidth = 0, $lineHeight = 5, $border = 0)`: Crea una celda con una etiqueta y un valor, utilizada para mostrar información en el acta. Usa `MultiCell` para admitir valores largos con ajuste de línea.
    *   `SectionTitle($title, $lineHeight = 6)`: Crea un título de sección con un formato específico (fondo gris, negrita).
    *   `Paragraph($text, $lineHeight = 4.5)`:  Agrega un párrafo de texto justificado al PDF.

**Flujo principal del script:**

1.  **Configuración y Autenticación:**
    *   Habilita la visualización de errores para depuración.
    *   Inicia una sesión.
    *   Realiza una comprobación de autenticación y restringe el acceso a la página basándose en roles de usuario (`admin`, `tecnico`, `registrador`, `auditor`).
2.  **Conexión a la Base de Datos:**
    *   Establece una conexión a la base de datos utilizando `backend/db.php`.
    *   Verifica la conexión y muestra un mensaje de error si falla.
    *   Establece el charset de la conexión a `utf8mb4`.
3.  **Validación de ID del Préstamo:**
    *   Obtiene el ID del préstamo de la URL (`$_GET['id_prestamo']`).
    *   Valida que el ID sea un entero positivo.
4.  **Consulta a la Base de Datos:**
    *   Ejecuta una consulta SQL para obtener los datos necesarios para el acta de devolución, uniendo tablas como `prestamos_activos`, `activos_tecnologicos`, `usuarios` (tanto el que presta como el que recibe), `tipos_activo` y `cargos`.
    *   Filtra los resultados para obtener solo préstamos con `estado_prestamo = 'Devuelto'`.
    *   Prepara la consulta para evitar inyecciones SQL.
    *   Ejecuta la consulta y obtiene los resultados en un array asociativo (`$datos_devolucion`).
    *   Cierra la conexión a la base de datos.
5.  **Creación del PDF:**
    *   Instancia la clase `PDF_Acta_Devolucion`.
    *   Define márgenes y configura el objeto PDF.
    *   Agrega una página al PDF.
6.  **Formateo de Datos:**
    *   Formatea la fecha de devolución en un formato legible (ej. "Popayán, 26 de Octubre de 2023").
7.  **Adición de Contenido al PDF:**
    *   Agrega secciones y datos al PDF utilizando los métodos de la clase `PDF_Acta_Devolucion` ( `SectionTitle`, `InfoCell`, `Paragraph`).  La información se divide en secciones como Información del Elemento Tecnológico, Detalles de la Devolución, Datos de Quien Devuelve, y Datos de Quien Recibe.
8.  **Espacios para Firmas:**
    *   Crea espacios predefinidos para las firmas de quien devuelve y quien recibe, incluyendo líneas para la firma y campos para el número de identificación (C.C.).
9.  **Generación y Envío del PDF:**
    *   Sanitiza el nombre del archivo PDF basándose en la serie del activo o el ID del préstamo.
    *   Limpia el buffer de salida (si hay contenido previo).
    *   Envía el PDF al navegador para que se descargue o visualice.

**Dependencias clave:**

*   **`backend/auth_check.php`:**  Archivo que contiene la lógica para la autenticación y autorización de usuarios. Proporciona la función `restringir_acceso_pagina`.
*   **`backend/db.php`:**  Archivo que contiene la información de conexión a la base de datos y establece la conexión.
*   **`lib/fpdf/fpdf.php`:**  Librería FPDF para la generación de archivos PDF.
*   **Función `to_iso_devolucion()`:**  Aunque definida en el propio archivo, es una dependencia lógica ya que asegura la correcta codificación de los caracteres para FPDF.
*   **Variables de sesión (`$_SESSION`)**:  Usadas para la autenticación del usuario.
*   **Variables GET (`$_GET`)**: Utilizada para obtener el `id_prestamo` necesario para generar el acta.
```

---

## Archivo: `repo_temporal/generar_acta_entrega_pdf.php`

```markdown
## Resumen de `repo_temporal/generar_acta_entrega_pdf.php`

**Propósito principal del archivo:**

El archivo `generar_acta_entrega_pdf.php` tiene como propósito generar un archivo PDF que representa un acta de entrega de activos tecnológicos.  Esta acta incluye información del activo, la persona que lo entrega, la persona que lo recibe y la fecha del evento.  El acta se genera a partir de datos almacenados en una base de datos MySQL.

**Descripción de sus funciones o clases:**

*   **`PDF_Acta` (Clase):**  Extiende la clase `FPDF` (de la librería fpdf) para personalizar la generación del PDF del acta.  Incluye las siguientes funciones:
    *   `to_iso($string)`: Convierte una cadena de texto de UTF-8 a ISO-8859-1 para asegurar una correcta visualización de caracteres especiales en el PDF.
    *   `Header()`: Define el encabezado del PDF, incluyendo el logo, título del proceso y otros datos informativos.
    *   `Footer()`: Define el pie de página del PDF, mostrando el número de página.
    *   `Draw_Checkbox($label, $is_checked)`:  Dibuja una casilla de verificación (checkbox) con una etiqueta.  Muestra una 'X' si la casilla está marcada (`$is_checked` es verdadero).
    *   `Draw_Signature_Block($label, $name, $cc = '')`: Dibuja un bloque de firma con el nombre, cédula (si está disponible) y espacio para la firma y fecha.
    *   `SetWidths($w)`: Establece los anchos de las columnas para las filas de datos.
    *   `Row($data, $line_height = 5)`:  Dibuja una fila de datos, asegurando el ajuste de texto dentro de las celdas y el salto de página si es necesario.
    *   `CheckPageBreak($h)`:  Verifica si hay suficiente espacio en la página antes de agregar una nueva fila.  Si no hay espacio, agrega una nueva página.
    *   `NbLines($w, $txt)`: Calcula el número de líneas que ocupará un texto dentro de un ancho determinado.

**Dependencias clave:**

*   **`backend/auth_check.php`:**  Se encarga de la autenticación del usuario.  Es probable que verifique si el usuario está logueado y tiene los permisos necesarios para acceder a esta funcionalidad.
*   **`backend/db.php`:**  Establece la conexión a la base de datos MySQL. Proporciona la variable `$conexion` (o `$conn`) que se utiliza para ejecutar consultas.
*   **`lib/fpdf/fpdf.php`:**  Librería FPDF para la generación de archivos PDF.  Se utiliza para crear el documento PDF, agregar contenido (texto, imágenes, líneas) y gestionar la estructura del documento.
*   **Session de PHP:** Se utiliza `session_start()` para poder utilizar las variables de sesión.

**Flujo general:**

1.  **Configuración:** Se configura el reporte de errores y se inicia la sesión.
2.  **Conexión a la base de datos:** Se incluye y verifica la conexión a la base de datos.
3.  **Validación del ID:** Se valida que el `id_historial` recibido por GET sea un entero válido.
4.  **Consulta a la base de datos:** Se realiza una consulta SQL para obtener los datos del evento, el activo, los usuarios responsables (quien entrega y quien recibe), y otros datos relevantes desde la tabla `historial_activos` y otras tablas relacionadas.
5.  **Verificación de datos:** Se verifica que la consulta haya devuelto resultados.
6.  **Preparación de datos:**  Se extraen los datos necesarios de la consulta y se asignan a variables.
7.  **Generación del PDF:**
    *   Se instancia la clase `PDF_Acta`.
    *   Se definen los márgenes y la fuente.
    *   Se agregan el encabezado, los datos del acta, la información del activo, las observaciones y los bloques de firma.
8.  **Salida del PDF:** Se genera la salida del PDF (en este caso, se muestra en el navegador) con un nombre de archivo basado en la serie del activo.
```

---

## Archivo: `repo_temporal/generar_acta_prestamo_pdf.php`

```markdown
## Resumen de `repo_temporal/generar_acta_prestamo_pdf.php`

**Propósito Principal:**

Este script PHP genera un acta de préstamo de un activo tecnológico en formato PDF.  Recupera los datos de la base de datos usando el ID del préstamo proporcionado en la URL y crea el documento PDF utilizando la librería FPDF. El PDF generado incluye información detallada sobre el activo, las condiciones del préstamo, y los datos de los usuarios que entregan y reciben el activo.

**Descripción de Funciones y Clases:**

1.  **Función `to_iso($string)`:**
    *   Convierte una cadena de texto de UTF-8 a ISO-8859-1. Esto es necesario porque la versión de FPDF utilizada podría no soportar UTF-8 directamente con fuentes estándar.

2.  **Clase `PDF_Acta_Prestamo extends FPDF`:**
    *   Extiende la clase `FPDF` para personalizar el documento PDF.
    *   **`Header()`:** Define el encabezado del PDF, incluyendo el logo de la empresa (ARPESOD ASOCIADOS SAS) y el título del acta.  Maneja un error si la ruta del logo es incorrecta.
    *   **`Footer()`:** Define el pie de página del PDF, incluyendo información sobre el sistema que lo generó y el número de página.
    *   **`InfoCell($label, $value, $labelWidth, $valueWidth, $lineHeight, $border)`:** Crea una celda con una etiqueta y su valor correspondiente. Utiliza `MultiCell` para permitir valores extensos que se ajusten al ancho de la celda.
    *   **`SectionTitle($title, $lineHeight)`:**  Crea un título de sección con un fondo gris.
    *   **`Paragraph($text, $lineHeight)`:** Crea un párrafo de texto justificado.

**Dependencias Clave:**

*   **`backend/auth_check.php`:**  Verifica la autenticación del usuario y restringe el acceso a la página según los roles permitidos (`admin`, `tecnico`, `registrador`, `auditor`).
*   **`backend/db.php`:**  Establece la conexión a la base de datos.
*   **`lib/fpdf/fpdf.php`:**  Librería FPDF para la generación de documentos PDF.
*   **Variables de Sesión:** Utiliza `session_start()` para acceder a variables de sesión (presumiblemente para la autenticación y autorización).
*   **`$_GET['id_prestamo']`:** El ID del préstamo se obtiene de la URL, lo cual es crítico para la consulta de la base de datos.
```

---

## Archivo: `repo_temporal/generar_acta_traslado_pdf.php`

```markdown
## Resumen del archivo 'repo_temporal/generar_acta_traslado_pdf.php'

**Propósito Principal:**

Este script PHP genera un acta de traslado de activos fijos en formato PDF. La información para generar el acta se extrae de la base de datos, basándose en el ID del historial de traslados proporcionado como parámetro GET.  El script utiliza la librería FPDF para crear el documento PDF y lo muestra directamente en el navegador.

**Descripción de Funciones y Clases:**

*   **Ninguna función definida por el usuario a excepción de los métodos de la clase `PDF_Acta`**:  El script se basa principalmente en ejecutar consultas SQL para obtener los datos necesarios. La lógica principal se encuentra en la clase `PDF_Acta`.
*   **Clase `PDF_Acta` (extiende `FPDF`):**  Esta clase personalizada extiende la clase `FPDF` para facilitar la creación del acta. Incluye los siguientes métodos:
    *   `to_iso($string)`: Convierte una cadena de UTF-8 a ISO-8859-1 para asegurar una correcta visualización de caracteres especiales en el PDF.
    *   `Header()`: Define el encabezado del PDF, incluyendo el logo, título y datos de la empresa.
    *   `Footer()`: Define el pie de página del PDF, mostrando el número de página.
    *   `Draw_Checkbox($label, $is_checked)`: Dibuja una casilla de verificación con una etiqueta asociada. La casilla se marca con una "X" si `$is_checked` es verdadero.
    *   `Draw_Signature_Block($label, $name, $cc = '')`:  Crea un bloque para la firma, incluyendo la etiqueta, el nombre y el número de cédula (CC).
    *   `SetWidths($w)`: Establece los anchos de las celdas para la función `Row`.
    *   `Row($data, $line_height = 5)`: Crea una fila de celdas con los datos proporcionados.  Ajusta la altura de la fila automáticamente para que quepa el texto.
    *   `CheckPageBreak($h)`: Verifica si hay espacio suficiente en la página actual y, si no, agrega una nueva página.
    *   `NbLines($w, $txt)`: Calcula el número de líneas que ocupará un texto dado en una celda de ancho específico.

**Dependencias Clave:**

*   **`backend/auth_check.php`**:  Verifica si el usuario está autenticado antes de permitir el acceso al script. Esto implica un sistema de autenticación implementado en el backend.
*   **`backend/db.php`**:  Establece la conexión a la base de datos.  La conexión debe estar configurada para usar UTF8MB4.
*   **`lib/fpdf/fpdf.php`**:  La librería FPDF (Free PDF) es la base para generar los documentos PDF.  La clase `PDF_Acta` extiende esta clase.
*   **Variables `$_GET['id_historial']`**: Se espera un parámetro GET llamado `id_historial` el cual debe ser un entero válido, que sirve para consultar la información del traslado de activos.
*   **Base de Datos (MySQL):**  El script se basa en una base de datos MySQL con al menos las siguientes tablas y campos:
    *   `historial_activos`:  Almacena el historial de los activos, incluyendo la información del traslado (`id_activo`, `fecha_evento`, `datos_nuevos`, `datos_anteriores`, `id_historial`, `tipo_evento`).
    *   `activos_tecnologicos`:  Almacena la información de los activos (`Codigo_Inv`, `serie`, `marca`, `id_tipo_activo`, `estado`, `id`).
    *   `tipos_activo`:  Almacena los tipos de activo (`nombre_tipo_activo`, `id_tipo_activo`).
    *   `usuarios`: Almacena la información de los usuarios (`usuario` - cedula, `nombre_completo`, `id_cargo`, `empresa`, `regional`).
    *   `cargos`: Almacena los cargos de los usuarios (`nombre_cargo`, `id_cargo`).

**Consideraciones adicionales:**

*   El script realiza validación básica del parámetro `id_historial` para prevenir inyección SQL, pero se debe asegurar la sanitización de los datos al ejecutar las consultas para proteger contra ataques más avanzados.
*   El script usa `die()` para manejar errores, lo cual puede ser poco amigable para el usuario. Se podría considerar un manejo de errores más robusto.
*   El uso de `htmlspecialchars()` para escapar el `id_historial` en el mensaje de error es una buena práctica de seguridad.
*   La clase `PDF_Acta` usa `mb_convert_encoding` para convertir cadenas UTF-8 a ISO-8859-1, lo cual puede ser problemático si la base de datos o la configuración del servidor no están correctamente configuradas para UTF-8.  Considerar usar UTF-8 directamente en el PDF si es posible.
*   La lógica de marcado de las casillas de estado (Bueno, Regular, Malo) se basa en comparaciones directas de cadenas.  Si los valores en la base de datos cambian, la lógica podría fallar.  Sería más robusto usar una enumeración o constantes.
```

---

## Archivo: `repo_temporal/generar_bash.php`

```markdown
## Resumen de `repo_temporal/generar_bash.php`

**Propósito Principal:**

El archivo `generar_bash.php` tiene como propósito principal generar un hash seguro de una contraseña proporcionada por el usuario, para luego ser utilizada en una base de datos. Está diseñado como un script de uso único, pensado para ser eliminado después de generar el hash de la contraseña.

**Descripción:**

El script realiza las siguientes acciones:

1.  **Define una variable para la contraseña:** Define la variable `$nueva_contrasena_admin`  que debe ser modificada por el usuario para establecer la nueva contraseña deseada.
2.  **Verifica si la contraseña está vacía:** Comprueba si la variable de la contraseña está vacía. Si lo está, detiene la ejecución con un mensaje de error.
3.  **Genera el hash de la contraseña:** Utiliza la función `password_hash()` de PHP para generar un hash seguro de la contraseña utilizando el algoritmo por defecto (`PASSWORD_DEFAULT`).
4.  **Verifica errores al generar el hash:** Comprueba si la generación del hash tuvo éxito. En caso de error, detiene la ejecución con un mensaje.
5.  **Muestra el hash generado:**  Imprime el hash generado en la salida, listo para ser copiado y pegado en la base de datos. Utiliza `htmlspecialchars()` para evitar posibles problemas de seguridad al mostrar el hash.
6.  **Verifica el hash (opcional):** Opcionalmente, realiza una verificación para asegurar que el hash generado es válido y coincide con la contraseña original utilizando la función `password_verify()`.  Muestra mensajes de éxito o error según el resultado de la verificación.

**Funciones/Clases:**

*   No define clases.
*   Utiliza funciones nativas de PHP:
    *   `password_hash()`: Genera un hash de la contraseña.
    *   `password_verify()`: Verifica si una contraseña coincide con un hash dado.
    *   `htmlspecialchars()`: Escapa caracteres especiales para evitar problemas de seguridad al mostrar texto HTML.
    *   `die()`: Detiene la ejecución del script y muestra un mensaje.
    *   `empty()`:  Verifica si una variable está vacía.

**Dependencias Clave:**

*   PHP: El script depende de PHP y de la extensión password hashing que está habilitada por defecto.  No tiene dependencias externas adicionales.
*   Configuración de PHP: Requiere que la configuración de PHP sea correcta para que la función `password_hash` funcione correctamente.
```

---

## Archivo: `repo_temporal/gestion_prestamos.php`

```markdown
## Resumen de `repo_temporal/gestion_prestamos.php`

### Propósito Principal del Archivo

El archivo `gestion_prestamos.php` gestiona los préstamos de activos tecnológicos dentro de una organización. Permite registrar nuevos préstamos, registrar devoluciones, y listar los préstamos existentes asociados al usuario actual. Incluye lógica para autorizar el acceso según el rol del usuario, interactuar con la base de datos y responder a peticiones AJAX para buscar activos.

### Descripción de Funciones y Clases

El archivo no define clases, pero contiene las siguientes funciones principales a través de su lógica procedural:

1.  **Autenticación y Autorización:**
    *   Verifica que el usuario haya iniciado sesión y tenga un rol autorizado para acceder a la página (admin, técnico, registrador, auditor).

2.  **Gestión de la Base de Datos:**
    *   Establece una conexión a la base de datos utilizando los scripts `backend/db.php`.
    *   Realiza consultas y actualizaciones a las tablas `prestamos_activos`, `activos_tecnologicos` y `usuarios`.
    *   Maneja errores de conexión y los muestra al usuario.

3.  **Manejo de Peticiones AJAX:**
    *   Responde a una petición AJAX (`accion_ajax=buscar_activos_por_cedula_responsable`) para buscar activos asociados a un usuario (responsable) específico.
    *   Retorna un JSON con la información de los activos encontrados, el nombre del responsable y un mensaje de estado.

4.  **Registro de Préstamos:**
    *   Procesa el formulario para registrar un nuevo préstamo.
    *   Valida los datos del formulario (activo, usuario receptor, fechas).
    *   Inserta un nuevo registro en la tabla `prestamos_activos`.
    *   Actualiza el estado y el responsable del activo en la tabla `activos_tecnologicos`.
    *   Registra un evento en el historial mediante la función `registrar_evento_historial()` importada desde `backend/historial_helper.php`.
    *   Utiliza transacciones para asegurar la integridad de los datos.

5.  **Registro de Devoluciones:**
    *   Procesa el formulario para registrar la devolución de un activo prestado.
    *   Valida los datos del formulario (ID del préstamo, fecha de devolución, estado del activo).
    *   Actualiza el registro del préstamo en la tabla `prestamos_activos`.
    *   Actualiza el estado y el responsable del activo en la tabla `activos_tecnologicos`.
    *   Registra un evento de finalización de préstamo en el historial mediante la función `registrar_evento_historial()`.
    *   Utiliza transacciones para asegurar la integridad de los datos.

6.  **Listado de Préstamos:**
    *   Obtiene una lista de préstamos asociados al usuario actual (ya sea como prestador o receptor).
    *   Muestra la lista en una tabla HTML.

7.  **Generación de Actas:**
    *   Proporciona enlaces para generar actas de préstamo y devolución en formato PDF utilizando scripts externos (`generar_acta_prestamo_pdf.php`, `generar_acta_devolucion_pdf.php`).

8. **Gestión de Modales (Frontend):**
   *  Abre modales de Bootstrap para la creación y devolución de préstamos, controlados por variables PHP y JavaScript.
   *  Incluye lógica para reabrir modales en caso de errores en el procesamiento del formulario.
   *  Gestiona la búsqueda de activos mediante AJAX y la actualización de los campos del formulario.
   *  Maneja la lógica de la interfaz de usuario, como mostrar/ocultar secciones y habilitar/deshabilitar botones.

### Dependencias Clave

*   **`backend/auth_check.php`:**  Gestiona la autenticación y autorización de los usuarios. Restringe el acceso a la página según el rol del usuario.
*   **`backend/db.php`:**  Establece la conexión a la base de datos.
*   **`backend/historial_helper.php`:** Contiene la función `registrar_evento_historial()` para registrar eventos en el historial de los activos.
*   **`session_start()`:** Utilizada para mantener el estado de la sesión del usuario.
*   **Bootstrap:**  Framework CSS para la interfaz de usuario, incluyendo modales, tablas y estilos generales.
*   **Archivos PDF externos (`generar_acta_prestamo_pdf.php`, `generar_acta_devolucion_pdf.php`):** Generan los documentos PDF con la información de los préstamos y devoluciones.
```

---

## Archivo: `repo_temporal/gestionar_activos.php`

```markdown
## Resumen del archivo `repo_temporal/gestionar_activos.php`

**Propósito Principal:**

El archivo `gestionar_activos.php` proporciona una interfaz para que los administradores gestionen los "tipos de activo" en una base de datos.  Permite crear, editar y eliminar tipos de activo, definiendo sus atributos como nombre, descripción, vida útil sugerida y si requieren campos específicos.

**Descripción de Funciones/Clases:**

El archivo no define clases.  En cambio, se basa en un flujo de script para realizar las siguientes funciones:

1.  **Autenticación y Autorización:**
    *   `session_start()`: Inicia la sesión para el manejo de usuarios.
    *   `require_once 'backend/auth_check.php'`: Incluye el script para verificar la autenticación del usuario.
    *   `restringir_acceso_pagina(['admin'])`:  Restringe el acceso a la página solo a usuarios con rol de "admin".

2.  **Conexión a la Base de Datos:**
    *   `require_once 'backend/db.php'`: Incluye el script para establecer la conexión a la base de datos.
    *   Manejo de errores de conexión y despliegue de un mensaje de alerta si la conexión falla.

3.  **Gestión de Mensajes:**
    *   Utiliza variables de sesión (`$_SESSION['mensaje_accion_gestion']`) para almacenar y mostrar mensajes de éxito o error después de realizar acciones.
    *   Prioriza mensajes de error de conexión sobre otros mensajes, mostrando el error de conexión si existe.

4.  **Lógica de Creación de Tipos de Activo (POST):**
    *   Procesa el formulario para crear un nuevo tipo de activo cuando se envía el formulario con el nombre `crear_tipo_activo_submit`.
    *   Valida que el nombre del tipo de activo no esté vacío y que no exista ya en la base de datos.
    *   Inserta el nuevo tipo de activo en la tabla `tipos_activo`.
    *   Muestra mensajes de éxito o error usando variables de sesión y redirige.
    *   Maneja errores en la inserción y los registra en el registro de errores del servidor.

5.  **Lógica de Edición de Tipos de Activo (POST):**
    *   Procesa el formulario para editar un tipo de activo existente cuando se envía el formulario con el nombre `editar_tipo_activo_submit`.
    *   Valida que se proporcione un ID y un nombre para la edición.
    *   Verifica que el nombre editado no esté en uso por otro tipo de activo.
    *   Actualiza el tipo de activo en la tabla `tipos_activo`.
    *   Muestra mensajes de éxito o error usando variables de sesión y redirige.
    *   Maneja errores en la actualización y los registra en el registro de errores del servidor.

6.  **Lógica de Eliminación o Carga para Edición (GET):**
    *   Procesa las solicitudes GET para eliminar un tipo de activo (`accion=eliminar`).
    *   Elimina el tipo de activo de la tabla `tipos_activo`.
    *   Muestra mensajes de éxito o error usando variables de sesión y redirige.
    *   Maneja errores en la eliminación (como claves foráneas) y los registra en el registro de errores del servidor.
    *   Procesa las solicitudes GET para cargar los datos de un tipo de activo para su edición (`accion=editar_tipo`).
    *   Recupera los datos del tipo de activo de la tabla `tipos_activo`.
    *   Establece una variable para abrir el modal de edición con los datos recuperados.
    *   Maneja el escenario donde el tipo de activo no se encuentra.

7.  **Listado de Tipos de Activo:**
    *   Recupera todos los tipos de activo de la tabla `tipos_activo` y los almacena en el array `$tipos_activo_listados` para su visualización en una tabla HTML.
    *   Ordena los resultados por nombre.
    *   Maneja errores en la consulta y los registra.

8.  **Presentación HTML:**
    *   Genera la interfaz de usuario (HTML) con Bootstrap para mostrar la lista de tipos de activo, los botones para crear y editar, y los modales para realizar estas acciones.
    *   Utiliza PHP para dinámicamente generar la tabla con los tipos de activo, los enlaces para editar y eliminar, y los campos de formulario en los modales.
    *   Utiliza JavaScript para controlar la apertura de los modales de creación y edición, dependiendo de si hubo errores previos en las acciones correspondientes.

**Dependencias Clave:**

*   **`backend/auth_check.php`:**  Responsable de la autenticación y autorización del usuario.  Define la función `restringir_acceso_pagina`.
*   **`backend/db.php`:** Responsable de la conexión a la base de datos. Define la variable `$conn` o `$conexion`.
*   **Base de Datos (MySQL):**  Necesita una base de datos MySQL con una tabla llamada `tipos_activo` con al menos las siguientes columnas:
    *   `id_tipo_activo` (INT, PRIMARY KEY, AUTO_INCREMENT)
    *   `nombre_tipo_activo` (VARCHAR)
    *   `descripcion` (TEXT)
    *   `vida_util_sugerida` (INT, NULLABLE)
    *   `campos_especificos` (BOOLEAN/TINYINT)
*   **Bootstrap 5:** Utilizado para el diseño de la interfaz de usuario y la funcionalidad de los modales.
*   **Bootstrap Icons:** Utilizadas para los iconos.
```

---

## Archivo: `repo_temporal/gestionar_cargos.php`

```markdown
## Resumen de `repo_temporal/gestionar_cargos.php`

**Propósito principal del archivo:**

Este script PHP proporciona una interfaz para la gestión de cargos (roles) dentro de un sistema. Permite a los administradores crear, editar y eliminar cargos, así como ver una lista de los cargos existentes.  La gestión incluye la validación de datos y la comprobación de dependencias (si un cargo está asignado a usuarios antes de permitir su eliminación).

**Descripción de sus funciones o clases:**

El archivo no define clases, sino que implementa la lógica directamente en un script PHP. Sus principales funcionalidades son:

*   **Autenticación y Autorización:** Verifica que el usuario actual tenga el rol de administrador antes de permitir el acceso a la página, utilizando `auth_check.php` y `restringir_acceso_pagina()`.
*   **Conexión a la base de datos:** Establece una conexión a la base de datos, manejando posibles errores de conexión y mostrando un mensaje de error si es necesario. Utiliza `backend/db.php` para la conexión.
*   **Gestión de Sesiones:** Utiliza sesiones para mantener información sobre el usuario actual (nombre, rol) y para mostrar mensajes de estado después de realizar acciones (creación, actualización, eliminación).
*   **Creación de Cargos:** Procesa el formulario de creación de cargos, validando los datos de entrada, verificando si el nombre del cargo ya existe, e insertando el nuevo cargo en la base de datos.
*   **Edición de Cargos:** Procesa el formulario de edición de cargos, validando los datos de entrada, verificando si el nuevo nombre del cargo ya existe (excepto para el cargo actual), y actualizando el cargo en la base de datos.
*   **Eliminación de Cargos:** Procesa la solicitud de eliminación de cargos, verificando si el cargo está asignado a algún usuario antes de permitir la eliminación.
*   **Listado de Cargos:** Consulta la base de datos para obtener una lista de todos los cargos existentes y los muestra en una tabla.
*   **Formato de título:** Implementa una función `formatoTitulo()` para estandarizar el formato de los nombres de los cargos.
*   **Control de Modales:** Controla la apertura de modales de creación y edición a través de variables booleanas y JavaScript.
*   **Manejo de Errores y Mensajes:**  Muestra mensajes de éxito o error al usuario después de realizar acciones, utilizando la variable de sesión `$_SESSION['mensaje_accion_cargos']`.

**Dependencias clave:**

*   **`backend/auth_check.php`:**  Responsable de la autenticación del usuario y la verificación de su rol.
*   **`backend/db.php`:**  Responsable de la conexión a la base de datos.
*   **Bootstrap CSS/JS:** Se utiliza para el diseño y la funcionalidad de la interfaz de usuario, incluyendo modales y alertas.
*   **Bootstrap Icons:**  Se utiliza para mostrar iconos en la interfaz de usuario.
```

---

## Archivo: `repo_temporal/gestionar_proveedores.php`

```markdown
## Resumen de `gestionar_proveedores.php`

**Propósito Principal:**

Este archivo PHP proporciona una interfaz para la gestión de proveedores dentro de una aplicación web. Permite a los administradores crear, editar y eliminar información de proveedores, almacenada en una base de datos. La interfaz incluye validación de datos, manejo de errores y mensajes de estado para el usuario.

**Descripción de Funciones/Clases:**

El archivo no define clases. Su funcionalidad se implementa a través de código PHP procedural, que incluye:

*   **Conexión a la base de datos:** Se conecta a la base de datos utilizando las credenciales definidas en `backend/db.php`. Maneja errores de conexión y muestra un mensaje al usuario si la conexión falla.
*   **Autenticación y autorización:** Verifica que el usuario actual tenga el rol de "admin" mediante `backend/auth_check.php`. Si no tiene el rol adecuado, se restringe el acceso a la página.
*   **Manejo de Sesiones:** Utiliza sesiones para mantener información del usuario y mensajes de estado.
*   **Procesamiento de Acciones POST (CRUD):**
    *   **Crear proveedor:** Recibe los datos del formulario para crear un nuevo proveedor, valida los datos (nombre obligatorio y formato de email), verifica si el nombre del proveedor ya existe y, si todo es correcto, inserta el nuevo proveedor en la base de datos.
    *   **Actualizar proveedor:** Recibe los datos del formulario para editar un proveedor existente, valida los datos, verifica si el nombre del proveedor ya existe (excluyendo el proveedor actual) y, si todo es correcto, actualiza la información del proveedor en la base de datos.
    *   **Eliminar proveedor:** Recibe el ID del proveedor a eliminar y lo elimina de la base de datos. Se incluye un comentario indicando la posibilidad de una verificación adicional para evitar la eliminación de proveedores que estén en uso.
*   **Carga de datos para editar (GET):** Si se recibe una solicitud GET con la acción "editar" y un ID de proveedor, se recupera la información del proveedor de la base de datos y se prepara para mostrarla en un formulario de edición.
*   **Listado de proveedores:** Recupera la lista de todos los proveedores de la base de datos y los muestra en una tabla.
*   **Presentación (HTML):** Genera la interfaz de usuario utilizando HTML, CSS y Bootstrap. Incluye formularios para crear y editar proveedores, una tabla para mostrar la lista de proveedores, y mensajes de estado para informar al usuario sobre el resultado de las acciones. Incluye modales para crear y editar proveedores.
*   **Manejo de errores:** Incluye manejo de errores con mensajes específicos para el usuario y logs para el administrador.

**Dependencias Clave:**

*   `backend/auth_check.php`: Archivo que contiene la lógica para la autenticación y autorización de usuarios.
*   `backend/db.php`: Archivo que contiene la información de conexión a la base de datos y posiblemente funciones relacionadas con la interacción con la base de datos.
*   Librería Bootstrap (CSS y JS): Para la maquetación y estilos de la interfaz de usuario.
*   Bootstrap Icons: Para los iconos mostrados en la interfaz.
*   Sesiones PHP: Para mantener el estado del usuario y los mensajes entre diferentes peticiones.
```

---

## Archivo: `repo_temporal/gestionar_roles.php`

```markdown
## Resumen de `repo_temporal/gestionar_roles.php`

**Propósito Principal:**

Este archivo PHP permite a un administrador gestionar los roles de usuario dentro de una aplicación.  Permite crear, editar y eliminar roles, controlando sus nombres y descripciones.  Gestiona la persistencia de estos roles en una base de datos MySQL.  La interfaz visual se construye con HTML y Bootstrap.

**Descripción de Funciones y Clases:**

Este archivo no define clases.  Implementa la lógica directamente en el script. Las principales funciones lógicas son:

*   **Conexión a la base de datos:** Se conecta a la base de datos utilizando el archivo `backend/db.php`.  Maneja errores de conexión mostrando un mensaje al usuario y registrando el error.
*   **Autenticación y Autorización:** Utiliza `backend/auth_check.php` para verificar si el usuario tiene permisos de administrador (`admin`) para acceder a la página. Restringe el acceso si no se cumple la condición.
*   **Creación de Roles (POST):** Procesa el formulario de creación de roles. Valida los datos (nombre obligatorio, nombre único), inserta el nuevo rol en la tabla `roles` y muestra un mensaje de éxito o error.  Redirige a la página de gestión de roles.
*   **Edición de Roles (POST):** Procesa el formulario de edición de roles. Valida los datos (nombre obligatorio, nombre único, ID válido), actualiza el rol en la tabla `roles` y muestra un mensaje de éxito o error.  Redirige a la página de gestión de roles.
*   **Eliminación de Roles (POST):** Procesa la solicitud de eliminación de roles.  Verifica si el rol está asignado a algún usuario antes de eliminarlo.  Impide la eliminación de roles predefinidos o críticos.  Elimina el rol de la tabla `roles` y muestra un mensaje de éxito o error. Redirige a la página de gestión de roles.
*   **Carga de Datos para Edición (GET):**  Si se recibe una solicitud GET con los parámetros `accion=editar` e `id`, recupera los datos del rol con el ID especificado de la tabla `roles` para mostrarlos en el formulario de edición.
*   **Listado de Roles:** Recupera todos los roles de la tabla `roles` y los muestra en una tabla HTML.
*   **Manejo de Mensajes:** Utiliza sesiones (`$_SESSION`) para almacenar y mostrar mensajes de éxito o error después de las acciones de creación, edición o eliminación. Los mensajes se muestran al usuario en forma de alertas Bootstrap.
*   **Control de apertura de modales:**  Utiliza flags booleanos `$abrir_modal_creacion_rol_js` y `$abrir_modal_editar_rol_js` y Javascript para controlar si los modales de creación o edición deben abrirse automáticamente al cargar la página (por ejemplo, después de un error de validación).

**Dependencias Clave:**

*   **`backend/auth_check.php`:**  Se encarga de la autenticación y autorización del usuario, restringiendo el acceso a la página a usuarios con el rol de administrador.
*   **`backend/db.php`:**  Establece la conexión a la base de datos MySQL.  Debe definir la variable `$conn` con la conexión activa.
*   **`$_SESSION`:**  Utilizada para gestionar la sesión del usuario y para almacenar mensajes flash (mensajes que se muestran una sola vez).
*   **Bootstrap (CSS y JS):** Framework CSS para el diseño de la interfaz de usuario.
*   **Bootstrap Icons:** Librería de íconos.
```

---

## Archivo: `repo_temporal/gestionar_usuarios.php`

```markdown
## Resumen del archivo `repo_temporal/gestionar_usuarios.php`

**Propósito principal:**

Este archivo PHP proporciona una interfaz para la gestión de usuarios dentro de una aplicación web. Permite a los administradores (y potencialmente a otros roles con permisos) crear, editar, activar/desactivar y eliminar cuentas de usuario. También maneja la autenticación y la restricción de acceso a la página según el rol del usuario actual.

**Descripción de funciones y clases:**

El archivo no define clases, pero contiene varias funciones y bloques de código clave:

*   **Autenticación y Autorización:**
    *   `session_start()`: Inicia una sesión PHP para mantener el estado del usuario.
    *   `require_once 'backend/auth_check.php'`: Incluye un archivo que probablemente contiene lógica para verificar si el usuario está autenticado.
    *   `restringir_acceso_pagina(['admin'])`:  Restringe el acceso a la página solo a usuarios con el rol de administrador.
*   **Conexión a la Base de Datos:**
    *   `require_once 'backend/db.php'`: Incluye un archivo que establece la conexión a la base de datos.
    *   Verifica y establece la conexión a la base de datos, mostrando un mensaje de error si falla.
    *   Establece el charset de la conexión a `utf8mb4`.
*   **Funciones de Formato y Utilidad:**
    *   `formatoTitulo($string)`: Convierte una cadena a formato de título (primera letra de cada palabra en mayúscula).
    *   `getRolBadgeClass($rol)`: Retorna la clase CSS de Bootstrap para un badge según el rol del usuario, permitiendo una visualización diferenciada de roles.
*   **Obtención de Datos para Formularios:**
    *   Realiza consultas a la base de datos para obtener listas de cargos, empresas y regionales, que se utilizan para poblar los menús desplegables en los formularios de creación y edición de usuarios.
    *   Define un array `$roles_form` con los roles posibles.
*   **Lógica POST (Crear, Actualizar, Eliminar):**
    *   Maneja las solicitudes POST para crear, editar y eliminar usuarios.
    *   **Crear Usuario:** Valida los datos del formulario, hashea la contraseña, verifica si el nombre de usuario ya existe y, si todo es correcto, inserta el nuevo usuario en la base de datos.
    *   **Editar Usuario:**  Valida los datos del formulario, verifica si el nombre de usuario ya existe (excepto para el mismo usuario que se está editando), y actualiza la información del usuario en la base de datos. También permite cambiar la contraseña.
    *   **Eliminar Usuario:**  Verifica que el usuario actual tenga el rol de administrador y que no esté intentando eliminarse a sí mismo o al administrador principal.  Verifica si el usuario a eliminar tiene activos asignados.  Si no tiene activos y el usuario actual es administrador, elimina el usuario de la base de datos.
*   **Lógica GET (Cargar Datos para Editar, Activar/Desactivar):**
    *   Maneja las solicitudes GET para cargar los datos de un usuario específico para editarlo o para activar/desactivar su cuenta.
    *   **Editar Usuario:** Obtiene la información del usuario a editar y la almacena en la variable `$usuario_para_editar`.
    *   **Activar/Desactivar Usuario:**  Cambia el estado de la cuenta del usuario (activo/inactivo) en la base de datos.
*   **Listado de Usuarios:**
    *   Realiza una consulta a la base de datos para obtener una lista de todos los usuarios.
*   **Interfaz de Usuario (HTML):**
    *   Genera la estructura HTML de la página, incluyendo:
        *   Una barra de navegación superior con información del usuario y un enlace para cerrar sesión.
        *   Un formulario para crear nuevos usuarios (dentro de un modal de Bootstrap).
        *   Una tabla que muestra la lista de usuarios con opciones para editar, eliminar y activar/desactivar cada usuario.
        *   Un formulario para editar usuarios (dentro de un modal de Bootstrap), que se muestra si se ha seleccionado un usuario para editar.
*   **JavaScript:**
    *   Muestra modales de Bootstrap.
    *   Realiza validaciones del lado del cliente en los formularios (por ejemplo, verificar que las contraseñas coincidan).
    *   Maneja la visualización condicional de los campos de cambio de contraseña en el formulario de edición.
    *   Controla que se abra automáticamente el modal de creación al recargar la página tras un error de creación.

**Dependencias Clave:**

*   **`backend/auth_check.php`:**  Este archivo es crucial para la autenticación y autorización. Se espera que contenga la lógica para verificar si un usuario está autenticado y cuál es su rol.
*   **`backend/db.php`:** Este archivo es responsable de establecer la conexión a la base de datos.
*   **Base de Datos:**  El script interactúa con una base de datos (presumiblemente MySQL) para almacenar y recuperar información de los usuarios.  Las tablas clave son `usuarios` y `cargos`.
*   **Sesiones PHP:** Se utiliza la funcionalidad de sesiones de PHP para mantener el estado del usuario autenticado.
*   **Bootstrap 5:** Se utiliza el framework CSS Bootstrap 5 para el diseño y la estructura de la interfaz de usuario, incluyendo modales y componentes de la tabla.
*   **Bootstrap Icons:** Se utilizan los iconos de Bootstrap Icons para mejorar la interfaz de usuario.

**Consideraciones:**

*   El código realiza validaciones básicas, pero se podrían agregar validaciones más robustas (tanto en el lado del cliente como en el servidor) para prevenir errores y mejorar la seguridad.
*   El código utiliza sentencias preparadas para prevenir inyecciones SQL, lo cual es una buena práctica de seguridad.
*   Los mensajes de error se registran en el registro de errores del servidor utilizando `error_log()`, lo cual es útil para la depuración.
*   Se emplean `htmlspecialchars()` para prevenir ataques XSS (Cross-Site Scripting).
*   Sería conveniente refactorizar el código para separarlo en funciones más pequeñas y reutilizables.
*   La funcionalidad de eliminar usuarios verifica si el usuario a eliminar tiene activos asignados.
```

---

## Archivo: `repo_temporal/guardar_activo.php`

```markdown
## Resumen del archivo `repo_temporal/guardar_activo.php`

**Propósito principal:**

Este archivo PHP es responsable de procesar la información enviada a través de un formulario (método POST) para registrar uno o más activos tecnológicos en la base de datos.  Realiza validaciones de datos, gestiona la transacción en la base de datos, registra el historial de creación de activos y actualiza la información del usuario responsable.  En caso de éxito o error, redirige al usuario a `index.php` con un mensaje correspondiente a través de la variable de sesión `$_SESSION`.

**Descripción de las funciones y lógica:**

1.  **Configuración inicial:**
    *   Habilita la visualización de errores.
    *   Inicia la sesión.
    *   Realiza una verificación de autenticación y autorización a través de `auth_check.php` y `restringir_acceso_pagina`. Solo los usuarios con roles de 'admin', 'tecnico' o 'registrador' pueden acceder.
    *   Incluye archivos de conexión a la base de datos (`backend/db.php`) y funciones de ayuda para el historial (`backend/historial_helper.php`).
    *   Define la constante `HISTORIAL_TIPO_CREACION`.

2.  **Conexión a la base de datos:**
    *   Verifica y establece la conexión a la base de datos, redirigiendo a `index.php` si falla.
    *   Establece el charset de la conexión a `utf8mb4`.

3.  **Procesamiento del formulario (método POST):**
    *   Recupera los datos del formulario, incluyendo la información del responsable del activo y los datos de cada activo en un lote.
    *   Realiza validaciones de los datos del formulario (campos obligatorios, tipo de datos, etc.).
    *   **Manejo de 'Aplicaciones Usadas':** Procesa la información sobre las aplicaciones usadas por el responsable. Permite seleccionar aplicaciones de una lista y especificar "Otros" si es necesario.
    *   **Obtención del ID del Usuario Responsable:** Busca el ID del usuario responsable en la tabla `usuarios` utilizando la cédula proporcionada.
    *   Inicia una transacción en la base de datos.
    *   **Iteración sobre los activos del lote:**
        *   Recupera los datos de cada activo del array `activos_lote`.
        *   Obtiene el ID del tipo de activo desde la tabla `tipos_activo`.
        *   Realiza validaciones específicas para cada activo (campos obligatorios, tipo de datos, etc.).
        *   Prepara y ejecuta la consulta SQL `INSERT` para insertar los datos del activo en la tabla `activos_tecnologicos`. Se usa prepared statements para prevenir inyección SQL.
        *   **Manejo de valores NULL para Codigo_Inv:** Si el campo `codigo_inv` del formulario está vacío, se guarda como `NULL` en la base de datos.
        *   Maneja excepciones durante la inserción, especialmente para claves duplicadas (serie o código de inventario) y otros errores de la base de datos.
        *   Registra un evento de historial utilizando la función `registrar_evento_historial` después de la creación exitosa de cada activo.
    *   **Actualización de Aplicaciones Usadas del Usuario:** Actualiza la columna `aplicaciones_usadas` en la tabla `usuarios` para el usuario responsable, si se proporcionaron aplicaciones.
    *   Realiza un `COMMIT` si todos los activos se guardaron correctamente, o un `ROLLBACK` si hubo errores.
    *   Establece mensajes de éxito o error en la variable de sesión `$_SESSION`.
    *   Redirige al usuario a `index.php`.

4.  **Acceso no permitido (método GET u otro):**
    *   Si el archivo se accede a través de un método diferente a POST, establece un mensaje de error y redirige a `index.php`.

**Dependencias clave:**

*   `backend/auth_check.php`:  Archivo para la autenticación y autorización de usuarios.
*   `backend/db.php`:  Archivo que contiene la lógica para la conexión a la base de datos.
*   `backend/historial_helper.php`: Archivo que contiene funciones para registrar eventos en el historial.
*   Tabla `usuarios`: Usada para buscar y actualizar la información del usuario responsable (específicamente el campo `aplicaciones_usadas`).
*   Tabla `activos_tecnologicos`:  La tabla principal donde se almacenan los datos de los activos.
*   Tabla `tipos_activo`: Usada para obtener el ID del tipo de activo.
*   Sesiones (`$_SESSION`):  Utilizadas para almacenar mensajes de error y éxito, así como para la autenticación.
```

---

## Archivo: `repo_temporal/guardar_usuario.php`

```markdown
## Resumen de `repo_temporal/guardar_usuario.php`

**Propósito principal:**

Este script procesa la solicitud de creación de un nuevo usuario. Recibe datos de un formulario (método POST), los valida, hashea la contraseña y guarda la información del usuario en la base de datos.  Gestiona la redirección apropiada al usuario una vez completado el proceso, mostrando mensajes de éxito o error. Admite la creación de usuarios tanto por usuarios administradores como por usuarios que se registran por sí mismos.

**Funciones y Clases:**

El script no define clases.  Utiliza funciones externas definidas en los archivos que incluye.  La lógica principal se encuentra directamente en el script.  Las operaciones clave son:

*   **Captura de Datos del Formulario:** Recopila la información del nuevo usuario del formulario enviado mediante el método POST.
*   **Validación de Datos:** Verifica la integridad y validez de los datos ingresados, asegurando que los campos obligatorios no estén vacíos, que las contraseñas coincidan y que tengan la longitud mínima requerida.
*   **Asignación de Rol:** Determina el rol del usuario a crear. Si el usuario actual es un administrador, se utiliza el rol seleccionado en el formulario. De lo contrario, el rol por defecto es 'registrador'.
*   **Procesamiento en Base de Datos:**
    *   Verifica si ya existe un usuario con la misma cédula (identificador único).
    *   Hashea la contraseña utilizando `password_hash`.
    *   Inserta los datos del nuevo usuario en la tabla `usuarios` de la base de datos.
*   **Redirección:**  Redirige al usuario a una página específica dependiendo de si la creación del usuario fue exitosa y del rol del usuario que está creando la cuenta. Un administrador es redirigido a `crear_usuario.php` para crear otro usuario, mientras que un usuario que se registra es redirigido a `login.php`.  En caso de error, redirige a la página que originó la solicitud (generalmente `registro.php` o `crear_usuario.php`) mostrando un mensaje de error.

**Dependencias Clave:**

*   **`backend/auth_check.php`:**  Se encarga de la autenticación y autorización.  Presumiblemente, este archivo verifica si hay una sesión activa y si el usuario tiene los permisos necesarios para realizar la acción (en este caso, crear un usuario).  Incluye la función `obtener_rol_usuario()` utilizada para determinar el rol del usuario actual.
*   **`backend/db.php`:**  Establece la conexión a la base de datos.  Proporciona la variable `$conn` o `$conexion` que contiene la conexión PDO o MySQLi.
*   **`$_SESSION`:** Utilizada para almacenar mensajes de error y éxito, así como la información del usuario actual.
*   **`password_hash()`:** Función nativa de PHP para hashear contraseñas.

**Consideraciones Adicionales:**

*   El script utiliza `htmlspecialchars()` para prevenir ataques XSS al mostrar el nombre de usuario en mensajes.
*   Realiza validaciones básicas del lado del servidor para asegurar la integridad de los datos.
*   Utiliza sentencias preparadas para prevenir ataques de inyección SQL.
*   Manejo de errores: Utiliza `$_SESSION` para mostrar mensajes de error al usuario y redirige a la página anterior.
```

---

## Archivo: `repo_temporal/historial.php`

```markdown
## Resumen del archivo `repo_temporal/historial.php`

**Propósito principal del archivo:**

El archivo `historial.php` tiene como propósito mostrar el historial de eventos asociados a un activo tecnológico específico.  Permite a los usuarios autorizados visualizar los cambios que ha sufrido un activo a lo largo del tiempo, incluyendo la fecha del evento, tipo de evento (creación, actualización, traslado, baja, etc.), descripción, usuario responsable y los datos anteriores y nuevos involucrados en el cambio.  También ofrece la posibilidad de generar actas de entrega o traslado para ciertos eventos.

**Descripción de sus funciones o clases:**

El archivo no define clases.  Principalmente contiene la función `getHistorialEventoBadgeClass()` y realiza las siguientes acciones:

*   **`getHistorialEventoBadgeClass($tipo_evento)`:**  Esta función recibe un tipo de evento del historial y devuelve la clase CSS de Bootstrap adecuada para mostrar un badge con un color que represente visualmente el tipo de evento (e.g., verde para creación, azul para traslado, etc.).

*   **Autenticación y Autorización:**  Verifica si el usuario ha iniciado sesión y, de no ser así, lo redirige a la página de inicio de sesión.

*   **Conexión a la base de datos:** Establece una conexión a la base de datos utilizando los datos proporcionados en `backend/db.php`.  Maneja errores de conexión.

*   **Validación de entrada:**  Valida el parámetro `id_activo` recibido por GET para asegurarse de que sea un entero positivo válido. Si no lo es, redirige al usuario a la página de búsqueda.

*   **Obtención de información del activo:**  Consulta la base de datos para obtener información básica del activo a partir de su `id`, incluyendo su tipo, serie, marca, y el nombre e información del responsable actual.

*   **Obtención del historial del activo:** Consulta la base de datos para obtener todos los eventos de historial asociados al activo especificado.  Los resultados se ordenan por fecha y ID de historial en orden descendente.

*   **Presentación de la información:**  Genera una página HTML que muestra la información del activo y su historial en un formato visualmente organizado, utilizando Bootstrap para el diseño y la función `getHistorialEventoBadgeClass` para resaltar los diferentes tipos de eventos.  También permite generar actas de entrega o traslado si el evento es de creación o traslado, respectivamente.  Finalmente, incluye la posibilidad de mostrar detalles de los datos modificados en cada evento.

**Dependencias clave:**

*   **`session_start()`:**  Utilizada para gestionar la sesión del usuario.
*   **`backend/auth_check.php`:**  (Crítica) Este archivo DEBE estar incluido primero y es responsable de la lógica de autenticación y autorización del usuario.
*   **`backend/db.php`:** (Crítica)  Este archivo contiene la información de conexión a la base de datos.
*   **`backend/historial_helper.php` (Implícito):** Aunque no se utiliza directamente en este archivo, el comentario `// auth_check.php DEBE estar primero` sugiere que otros archivos en el directorio `backend/` también son importantes para la funcionalidad de la aplicación.
*   **Bootstrap:** Framework CSS para el diseño de la interfaz de usuario.
*   **Bootstrap Icons:** Conjunto de iconos utilizados en la interfaz.
*   **Funciones PHP:**  `isset()`, `filter_var()`, `(int)`, `htmlspecialchars()`, `date()`, `json_decode()`, `nl2br()` y otras funciones nativas de PHP.

**Notas adicionales:**

*   El código incluye manejo de errores para la conexión a la base de datos y las consultas SQL.
*   Se utilizan sentencias preparadas para prevenir ataques de inyección SQL.
*   Se utilizan constantes para definir los tipos de eventos del historial, lo que mejora la legibilidad y mantenibilidad del código.
*   La interfaz de usuario está diseñada para ser imprimible.
*   El código incluye mensajes de error y alertas informativas para el usuario.
```

---

## Archivo: `repo_temporal/index.php`

```markdown
## Resumen de `repo_temporal/index.php`

### Propósito principal del archivo:

Este archivo PHP sirve como una interfaz para registrar activos por lote, asignándolos a un responsable.  Permite ingresar información del responsable, agregar varios activos a una lista, y luego guardar todos los activos asociados a ese responsable en una base de datos. El archivo gestiona la autenticación del usuario, la autorización basada en roles, la conexión a la base de datos, la lectura de opciones predefinidas desde la base de datos, la validación de entrada, y la presentación de la interfaz de usuario con Bootstrap.

### Descripción de sus funciones y clases:

El archivo no define clases explícitas, sino que funciona como un script procedural. Las principales funcionalidades se pueden agrupar en las siguientes secciones:

*   **Autenticación y Autorización:** Verifica si el usuario está autenticado y tiene el rol necesario para acceder a la página.  Utiliza `auth_check.php` para este propósito y restringe el acceso usando `restringir_acceso_pagina()`.
*   **Conexión a la base de datos:** Establece una conexión a la base de datos utilizando el script `backend/db.php`.  Verifica que la conexión se haya establecido correctamente y configura el charset a `utf8mb4`.
*   **Lectura de datos desde la base de datos:** Consulta la tabla `tipos_activo` para obtener los nombres de los tipos de activos y su vida útil sugerida.  Si la consulta falla, proporciona valores predeterminados.
*   **Definición de opciones para el formulario:** Define arrays con opciones predefinidas para los selects del formulario (regionales, empresas, tipo de equipo, etc.).
*   **Procesamiento de mensajes globales:**  Recupera y muestra mensajes globales y errores almacenados en la sesión (por ejemplo, después de un intento de guardar datos).
*   **Generación de la interfaz de usuario (HTML):**  Crea la interfaz HTML utilizando Bootstrap, incluyendo un formulario para ingresar la información del responsable y los activos.  Incluye validación en el lado del cliente con JavaScript.
*   **Lógica de JavaScript:** El script contiene una gran cantidad de código Javascript que se encarga de:
    *   Controlar la visibilidad de las secciones del formulario.
    *   Validar la entrada del usuario.
    *   Agregar y eliminar activos de una tabla dinámica.
    *   Enviar los datos al servidor mediante una solicitud AJAX.
    *   Buscar datos del responsable mediante AJAX.
    *   Gestionar la lógica del campo condicional del tipo de impresora.
    *   Manejo de la selección de aplicaciones del responsable.
*   **Guardado de datos (se delega a `guardar_activo.php`):** Al presionar "Guardar Todo", el script recopila todos los datos del formulario y de la tabla de activos, los prepara y los envía al script `guardar_activo.php` para su procesamiento y almacenamiento en la base de datos. Este envío se realiza mediante la creación dinámica de campos ocultos en el formulario.

### Dependencias clave:

*   **`backend/auth_check.php`:**  Gestiona la autenticación y autorización del usuario.
*   **`backend/db.php`:** Establece la conexión a la base de datos.
*   **Base de datos:**  Se utiliza una base de datos MySQL (o compatible) para almacenar la información de los tipos de activos, la información del usuario (para autocompletar los datos del responsable) y los datos de los activos que se van a registrar.
*   **Bootstrap:**  Se utiliza Bootstrap para el diseño de la interfaz de usuario.
*   **Bootstrap Icons:** Se usa la librería de íconos de Bootstrap.
*   **JavaScript:** Se usa JavaScript para la manipulación del DOM, la validación de la entrada del usuario y la comunicación con el servidor (AJAX).
*   **`guardar_activo.php`:** Recibe los datos y se encarga de guardarlos en la base de datos.
*   **`buscar_datos_usuario.php`:** Recibe la cédula del responsable y retorna la información del usuario desde la base de datos.

```

---

## Archivo: `repo_temporal/informes.php`

```markdown
## Resumen del archivo `informes.php`

### Propósito Principal:

El archivo `informes.php` es una página web que genera informes sobre activos tecnológicos. Permite a los usuarios (administradores, técnicos y auditores) seleccionar diferentes tipos de informes (general, por tipo, por estado, por regional, por empresa, activos dados de baja, movimientos recientes, activos en mantenimiento y activos en préstamo) y filtrarlos por rangos de fecha.  Los informes se muestran en formato HTML y se pueden exportar a Excel.

### Descripción de Funciones y Clases:

El archivo no define clases, pero contiene las siguientes funciones:

*   **`getEstadoBadgeClass($estado)`**:  Recibe un estado de activo como entrada y devuelve la clase CSS de Bootstrap correspondiente para un badge (etiqueta visual) que indica el estado. Maneja varios estados como 'asignado', 'en mantenimiento', 'dado de baja', etc.  Retorna un badge por defecto si el estado no coincide con ninguno de los casos predefinidos.
*   **`displayStars($rating, $totalStars = 5)`**: Recibe una calificación numérica (rating) y genera una representación visual de estrellas (★ y ☆) basada en esa calificación. Permite mostrar la calificación de satisfacción de un activo.
*   Define constantes como `HISTORIAL_TIPO_MANTENIMIENTO`, `HISTORIAL_TIPO_BAJA`, `HISTORIAL_TIPO_TRASLADO`, `HISTORIAL_TIPO_ASIGNACION_INICIAL`, `HISTORIAL_TIPO_CREACION`, `HISTORIAL_TIPO_REACTIVACION` si no están definidas, que se utilizan en las consultas SQL para filtrar por tipos de eventos en el historial de activos.

Además, el archivo incluye lógica para:

*   **Autenticación y Autorización:** Verifica si el usuario está autenticado y tiene los permisos necesarios para acceder a la página, utilizando `auth_check.php` y la función `restringir_acceso_pagina`.
*   **Conexión a la Base de Datos:** Establece una conexión a la base de datos utilizando el archivo `db.php`. Maneja errores de conexión.
*   **Obtención y validación de parámetros de entrada:** Obtiene el tipo de informe seleccionado y el rango de fechas desde los parámetros GET.
*   **Construcción Dinámica de Consultas SQL:** Construye las consultas SQL dinámicamente en función del tipo de informe seleccionado y el rango de fechas. Utiliza sentencias preparadas para prevenir inyecciones SQL.
*   **Ejecución de Consultas y Recuperación de Datos:** Ejecuta las consultas SQL preparadas y recupera los resultados.
*   **Presentación de Datos:** Formatea y muestra los datos en una tabla HTML. Implementa una lógica de renderizado condicional basada en el tipo de informe seleccionado. Incluye funciones para formatear la salida, como `getEstadoBadgeClass` y `displayStars`.
*   **Exportación a Excel:** Proporciona un enlace para exportar los datos del informe a un archivo Excel.
*   **Filtros de Fecha:** Permite filtrar los informes por un rango de fechas (desde y hasta).
*   **Manejo de Sesiones:** Utiliza sesiones para mantener la información del usuario.
*   **Mensajes de Error:** Muestra mensajes de error en caso de problemas de conexión a la base de datos o al ejecutar las consultas.

### Dependencias Clave:

*   **`backend/auth_check.php`**:  Gestiona la autenticación y autorización de usuarios. Define la función `restringir_acceso_pagina` para controlar el acceso a la página según el rol del usuario.
*   **`backend/db.php`**:  Establece la conexión a la base de datos.
*   **Librería Bootstrap (CSS y JS)**: Proporciona estilos y componentes de interfaz de usuario.
*   **Librería Bootstrap Icons**: Proporciona iconos para la interfaz de usuario.
*   **`exportar_excel.php`**: Script externo que maneja la exportación de los datos a formato Excel.
```

---

## Archivo: `repo_temporal/login.php`

```markdown
## Resumen del archivo `repo_temporal/login.php`

**Propósito principal:**

El archivo `login.php` es la página de inicio de sesión para un sistema de inventario de activos. Permite a los usuarios autenticarse utilizando su usuario y contraseña contra una base de datos, estableciendo una sesión y redirigiéndolos a la página principal (`menu.php`) si la autenticación es exitosa.  También proporciona un enlace para registrarse como "Registrador".

**Descripción de funciones y clases:**

El archivo `login.php` no define clases ni funciones personalizadas.  Su lógica se centra en el siguiente flujo:

1.  **Inicio de sesión y redirección (si ya autenticado):** Inicia una sesión PHP.  Verifica si ya existe una sesión activa (`$_SESSION["loggedin"]`). Si es así, redirige al usuario a `menu.php`.

2.  **Conexión a la base de datos:** Incluye el archivo `backend/db.php`, el cual se espera que establezca una conexión a la base de datos y la almacene en la variable `$conn`.  Si `$conn` existe pero `$conexion` no está definida, asigna `$conn` a `$conexion`. Esto permite una compatibilidad con código antiguo que usa `$conexion`.

3.  **Procesamiento del formulario de inicio de sesión (POST):**
    *   Verifica si el formulario ha sido enviado (método POST y `isset($_POST['login_submit'])`).
    *   Valida si los campos usuario y contraseña están vacíos.  Si lo están, muestra un mensaje de error.
    *   Si los campos no están vacíos, se obtienen los valores del usuario y contraseña desde el formulario.
    *   Verifica si la conexión a la base de datos `$conexion` es exitosa. Si hay un error, muestra un mensaje.
    *   Si la conexión es exitosa, prepara una consulta SQL para buscar al usuario en la base de datos. La consulta recupera información del usuario (id, usuario, clave hash, nombre completo, rol, estado activo, nombre del cargo, empresa, regional) uniendo las tablas `usuarios` y `cargos`.
    *   Ejecuta la consulta preparada.
    *   Si se encuentra un usuario con el usuario proporcionado:
        *   Obtiene los resultados de la consulta.
        *   Verifica si la cuenta de usuario está activa (`activo_db == 1`).
        *   Verifica si la contraseña proporcionada coincide con el hash almacenado en la base de datos usando `password_verify()`.
        *   Si la cuenta está activa y la contraseña es correcta:
            *   Regenera el ID de sesión para prevenir la fijación de sesión.
            *   Establece variables de sesión (`$_SESSION`) con información del usuario autenticado.
            *   Redirige al usuario a la página `menu.php`.
        *   Si la contraseña es incorrecta o la cuenta está inactiva, muestra un mensaje de error.
    *   Si no se encuentra ningún usuario con el usuario proporcionado, muestra un mensaje de error.
    *   Cierra la declaración preparada (`$stmt->close()`).
4.  **HTML:**
    *   Muestra un formulario HTML para el inicio de sesión, incluyendo campos para usuario y contraseña.
    *   Muestra mensajes de error, si los hay.
    *   Incluye enlaces a hojas de estilo CSS de Bootstrap y Bootstrap Icons para el diseño visual.
    *   Incluye un enlace a `registro.php` para nuevos registradores.
    *   Importa el bundle de JavaScript de Bootstrap.

**Dependencias clave:**

*   **`backend/db.php`:**  Se espera que este archivo establezca la conexión a la base de datos y defina la variable `$conexion` (o `$conn`).  Sin este archivo, el inicio de sesión no puede funcionar.
*   **Base de datos:** Requiere una base de datos MySQL (o similar) con una tabla llamada `usuarios` que contenga al menos las columnas `id`, `usuario`, `clave` (almacenada como un hash), `nombre_completo`, `rol`, `activo`, `id_cargo`, `empresa` y `regional`.  También requiere una tabla `cargos` con al menos `id_cargo` y `nombre_cargo`.
*   **`session_start()`:** Utiliza sesiones PHP para mantener el estado de inicio de sesión del usuario.
*   **`password_verify()`:** Utiliza esta función para verificar la contraseña ingresada contra el hash almacenado en la base de datos.  Esto implica que las contraseñas se almacenan de forma segura (hasheadas) usando `password_hash()` en el proceso de registro o creación de usuarios.
*   **Bootstrap CSS/JS:** Utiliza Bootstrap para el diseño y la funcionalidad de la interfaz de usuario.
*   **Bootstrap Icons:** Utiliza Bootstrap Icons para iconos dentro del formulario.
```

---

## Archivo: `repo_temporal/logout.php`

```markdown
## Resumen de `repo_temporal/logout.php`

**Propósito Principal:**

El archivo `logout.php` tiene como propósito principal finalizar la sesión del usuario actual y redirigirlo a la página de inicio de sesión (`login.php`).  En otras palabras, implementa la funcionalidad de "cerrar sesión".

**Descripción de Funciones:**

El script realiza las siguientes acciones:

1.  **`session_start();`**:  Inicia una sesión existente o recupera una existente si ya existe. Es fundamental para poder interactuar con las variables de sesión.
2.  **`session_destroy();`**:  Destruye todos los datos asociados con la sesión actual.  Esto elimina las variables de sesión (como el nombre de usuario, el estado de inicio de sesión, etc.) que se han almacenado para el usuario.
3.  **`header("Location: login.php");`**: Envía una cabecera HTTP al navegador para redirigir al usuario a la página `login.php`. Esto hace que el navegador cargue la página de inicio de sesión inmediatamente después de que se destruye la sesión.
4.  **`exit;`**:  Termina la ejecución del script. Esto asegura que no se ejecute ningún otro código después de la redirección, lo cual es una buena práctica.

**Dependencias Clave:**

*   **Sessiones de PHP:** Depende del sistema de gestión de sesiones de PHP (a través de `session_start()` y `session_destroy()`).
*   **`login.php`:** Depende de la existencia del archivo `login.php` al cual redirecciona.  Este archivo es crucial porque maneja la presentación del formulario de inicio de sesión.

**En resumen:** El archivo `logout.php` es un script sencillo pero importante que finaliza la sesión del usuario y lo redirige a la página de inicio de sesión, proporcionando una forma segura y controlada de cerrar la sesión en una aplicación web.
```

---

## Archivo: `repo_temporal/mantenimiento.php`

```markdown
## Resumen del archivo `repo_temporal/mantenimiento.php`

**Propósito Principal:**

Este archivo PHP proporciona una interfaz para registrar y finalizar el mantenimiento de activos tecnológicos. Permite buscar un activo por su número de serie, registrar información sobre el mantenimiento (diagnóstico, fecha, costo, etc.), registrar si el mantenimiento ha sido completado, dar de baja el activo si es necesario, y mantener un historial de estas acciones.  Está diseñado para ser usado por administradores y técnicos.

**Descripción de Funciones y Clases:**

*   **`fetch_activo_completo($db_conn, $serie_o_id, $es_id = false)`:**  Esta función realiza una consulta a la base de datos para obtener la información completa de un activo, ya sea buscándolo por su número de serie o por su ID.  Utiliza prepared statements para prevenir inyección SQL.
*   **No hay clases definidas en este archivo.**

**Variables Clave:**

*   `$serie_buscada`:  Almacena el número de serie del activo que se está buscando. Se obtiene de la petición GET.
*   `$activo_encontrado`:  Almacena los datos del activo encontrado, obtenidos de la base de datos a través de la función `fetch_activo_completo`.
*   `$activo_esta_en_mantenimiento`:  Indica si el activo encontrado ya está en estado de mantenimiento.
*   `$opciones_diagnostico`:  Un array que define las opciones disponibles para el diagnóstico del mantenimiento.
*   `$opciones_motivo_baja`:  Un array que define las opciones disponibles para el motivo de la baja del activo.
*   `$estados_finales_operativos`:  Un array que define los posibles estados finales de un activo después del mantenimiento.
*   `$proveedores`:  Un array que contiene los proveedores de mantenimiento obtenidos de la base de datos.
*   `$tecnicos_internos`: Un array que contiene los tecnicos internos que pueden hacer el mantenimiento, se obtienen de la base de datos.
*   `$mensaje`, `$error_mensaje`: Variables de sesión para almacenar mensajes de éxito o error que se muestran al usuario.
*   `$conexion`: Objeto de conexión a la base de datos.

**Dependencias Clave:**

*   **`backend/auth_check.php`:**  Gestiona la autenticación y autorización de usuarios.  La función `restringir_acceso_pagina` restringe el acceso a la página a los roles 'admin' y 'tecnico'.
*   **`backend/db.php`:**  Establece la conexión a la base de datos.
*   **`backend/historial_helper.php`:** Proporciona funciones para registrar eventos en el historial del sistema, como `registrar_evento_historial`.  También define constantes para los tipos de historial.
*   **`session_start()`:** Utilizada para la gestión de sesiones de usuario, almacenando información como el nombre de usuario, el rol y el ID de usuario.
*   **Funciones PHP:**  Varias funciones PHP estándar son utilizadas, como `trim()`, `isset()`, `empty()`, `filter_input()`, `htmlspecialchars()`, `error_log()`, `header()`, `urlencode()`,  `number_format()`, `date()`, `array_filter()`, `reset()`, `in_array()`.

**Flujo General:**

1.  **Autenticación y Autorización:** Verifica que el usuario esté autenticado y tenga los permisos necesarios.
2.  **Conexión a la Base de Datos:** Establece la conexión a la base de datos.
3.  **Búsqueda de Activo:** Permite al usuario buscar un activo por su número de serie.
4.  **Mostrar Información del Activo:** Si se encuentra el activo, muestra su información.
5.  **Registro/Finalización de Mantenimiento:**  Presenta un formulario para registrar un nuevo mantenimiento o finalizar uno existente.
6.  **Dar de Baja:** Permite dar de baja el activo si es necesario.
7.  **Historial:** Registra todas las acciones realizadas en el historial del sistema.
8.  **Redirección:** Redirige al usuario a la misma página después de realizar una acción.
9.  **Interfaz de Usuario:** Muestra mensajes de éxito/error y los formularios correspondientes.

**Seguridad:**

*   Utiliza prepared statements para prevenir inyección SQL en la función `fetch_activo_completo`.
*   Escapa la salida HTML con `htmlspecialchars()` para prevenir XSS.
*   Verifica los roles de usuario antes de permitir el acceso a ciertas funcionalidades.

**Mejoras Potenciales:**

*   Validación más robusta de los datos de entrada.
*   Manejo de errores más detallado.
*   Refactorización del código para mejorar la legibilidad y el mantenimiento.
*   Implementación de un sistema de logging más completo.
```

---

## Archivo: `repo_temporal/menu.php`

```markdown
## Resumen del archivo `repo_temporal/menu.php`

**Propósito principal del archivo:**

El archivo `menu.php` funciona como el menú principal de un sistema de inventario.  Muestra una interfaz con enlaces a diferentes funcionalidades del sistema, adaptando las opciones mostradas según los permisos del usuario autenticado.

**Descripción de sus funciones o clases:**

El archivo `menu.php` no define clases ni funciones propias directamente. Sin embargo, utiliza funciones externas para determinar los permisos del usuario, y renderiza una interfaz HTML que presenta las opciones del menú.

*   **Interfaz de Usuario:** El archivo renderiza una página HTML que presenta un menú de opciones para el sistema de inventario. Utiliza Bootstrap para el diseño y presenta las opciones como tarjetas (cards).
*   **Autenticación y Autorización:** Inicia una sesión PHP y requiere el archivo `backend/auth_check.php`, el cual presumiblemente contiene la lógica para verificar la autenticación del usuario y para determinar sus permisos.
*   **Manejo de Sesión:** Utiliza variables de sesión (`$_SESSION`) para obtener el nombre y rol del usuario actual. Si estas variables no están definidas, asigna valores por defecto ("Usuario" y "Desconocido", respectivamente).
*   **Control de Acceso Basado en Roles (RBAC):** Utiliza una función llamada `tiene_permiso_para()` (definida probablemente en `backend/auth_check.php`) para mostrar u ocultar las opciones del menú según los permisos asociados al rol del usuario. Esto permite que diferentes usuarios vean diferentes opciones en el menú, dependiendo de sus privilegios.
*   **Funcionalidad de Cerrar Sesión:**  Incluye un formulario que al ser enviado, redirige a `logout.php` para finalizar la sesión del usuario.
*   **Alerta de Error de Acceso:** Verifica si existe la variable de sesión `$_SESSION['error_acceso_pagina']` para mostrar una alerta de error en caso de que el usuario intente acceder a una página sin los permisos necesarios.
*   **Chatbot Integration:**  Implementa la funcionalidad de un chatbot mediante un iframe que apunta a `https://asistenteaifront.onrender.com/`. El chatbot se muestra y oculta mediante JavaScript al hacer clic en un botón.

**Dependencias clave:**

*   **`backend/auth_check.php`:**  Este archivo es fundamental, ya que se encarga de la autenticación del usuario y la verificación de permisos (autorización).  Se asume que define la función `tiene_permiso_para()`.
*   **Bootstrap (CSS y JS):**  Se utiliza para el diseño de la interfaz de usuario, incluyendo la estructura de la página, la barra de navegación, las tarjetas de menú y las alertas.
*   **Bootstrap Icons:**  Se utiliza para mostrar iconos en el menú y en la interfaz de usuario.
*   **`logout.php`:** Se encarga de cerrar la sesión del usuario.  No se incluye el código, pero es una dependencia necesaria para la funcionalidad de cierre de sesión.
*   **Variables de Sesión (`$_SESSION`):**  Utilizadas para mantener la información del usuario (nombre, rol, mensajes de error) entre las páginas.
*   **`https://asistenteaifront.onrender.com/`:** URL del chatbot.

En resumen, `menu.php` actúa como el punto de entrada principal del sistema, presentando un menú dinámico basado en los permisos del usuario actual, gestionando la sesión del usuario y proporcionando enlaces a las diferentes funcionalidades del sistema.
```

---

## Archivo: `repo_temporal/registro.php`

```markdown
## Resumen de `registro.php`

**Propósito Principal:**

El archivo `registro.php` es una página pública que permite a los usuarios registrarse en el sistema.  Proporciona un formulario para que los usuarios ingresen sus datos personales, como cédula, nombre, contraseña, cargo, empresa y regional.  Valida la confirmación de contraseña en el cliente con JavaScript y envía los datos a `guardar_usuario.php` para su procesamiento y almacenamiento en la base de datos.  También maneja mensajes de éxito y error (flash messages) mediante la sesión y muestra un modal si la cédula ingresada ya existe.

**Descripción de Funciones/Clases:**

*   **`formatoTitulo($string)`:** Función que convierte una cadena de texto a formato título (primera letra de cada palabra en mayúscula).  Utiliza `mb_convert_case` para soportar caracteres UTF-8 correctamente.

**Variables Globales:**

*   `$conexion`: Objeto de conexión a la base de datos.
*   `$conexion_error_msg`: Almacena mensajes de error de conexión a la base de datos.
*   `$regionales_usuarios`:  Array que define las regiones disponibles para los usuarios.
*   `$empresas_usuarios`: Array que define las empresas disponibles para los usuarios.
*   `$rol_fijo_para_registro`: Define el rol fijo que se asignará a los nuevos usuarios registrados ('registrador').
*   `$cargos_disponibles`: Array que almacena los cargos disponibles desde la base de datos.
*   `$mensaje_exito_registro`: Almacena el mensaje de éxito para mostrarlo después del registro.
*   `$error_general_registro`: Almacena mensajes de error generales relacionados con el registro.
*   `$mostrar_modal_cedula_existente`: Variable booleana que controla si se debe mostrar el modal de cédula existente.
*   `$mensaje_para_modal`: Almacena el mensaje a mostrar en el modal de cédula existente.

**Lógica Principal:**

1.  **Inicio de Sesión:** Inicia una sesión PHP (`session_start()`).
2.  **Conexión a la Base de Datos:** Incluye el archivo `backend/db.php` para establecer la conexión a la base de datos.  Maneja errores de conexión y almacena el mensaje de error en `$conexion_error_msg`. Define el charset de la conexión como `utf8mb4`.
3.  **Carga de Cargos:** Realiza una consulta a la base de datos para obtener la lista de cargos disponibles y los guarda en el array `$cargos_disponibles`.
4.  **Mensajes Flash:** Recupera mensajes de éxito y error almacenados en la sesión (`$_SESSION`) y los muestra en la página.  Utiliza `unset()` para eliminar estos mensajes de la sesión después de mostrarlos, evitando que aparezcan en futuras visitas.
5.  **Modal de Cédula Existente:**  Verifica si hay un error específico relacionado con la cédula ya existente en la base de datos.  Si es así, establece las variables necesarias para mostrar un modal con un mensaje informativo.
6.  **Formulario de Registro:** Muestra el formulario HTML para que el usuario ingrese sus datos. El formulario se muestra solamente si no existe un mensaje de éxito.
7.  **Validación de Contraseña (Cliente):** Incluye JavaScript para validar que la contraseña y la confirmación de contraseña coincidan.
8.  **Modal (HTML):** Define el HTML para el modal que se muestra si la cédula ya existe.  El modal solo se muestra si la variable `$mostrar_modal_cedula_existente` es verdadera.
9.  **JavaScript para Modal:** Incluye Javascript para mostrar el modal de cédula existente, si es necesario.

**Dependencias Clave:**

*   **`backend/db.php`:**  Archivo que contiene la lógica para establecer la conexión a la base de datos.
*   **`guardar_usuario.php`:**  Archivo que procesa los datos del formulario y guarda el nuevo usuario en la base de datos.
*   **Bootstrap 5:** Framework CSS para el diseño de la interfaz de usuario.
*   **Bootstrap Icons:** Librería de iconos para Bootstrap.

**Consideraciones de Seguridad:**

*   Se utiliza `htmlspecialchars()` para prevenir ataques XSS al mostrar mensajes de éxito y error.
*   Se utiliza `json_encode()` para pasar variables PHP a JavaScript de forma segura.
*   Se validan las contraseñas en el lado del cliente para asegurar que coinciden.  (Es importante también validarlas en el servidor en `guardar_usuario.php`).

**Mejoras Potenciales:**

*   Validación más robusta de los datos del formulario en el lado del servidor (en `guardar_usuario.php`).
*   Implementación de medidas de seguridad adicionales, como la protección contra ataques CSRF.
*   Añadir la opción de mostrar un mensaje de error si la carga de cargos falla.
*   Agregar validación del formato de la cédula en el cliente y en el servidor.
```

---

## Archivo: `repo_temporal/backend/auth_check.php`

```markdown
## Resumen del archivo `repo_temporal/backend/auth_check.php`

**Propósito Principal:**

Este archivo PHP tiene como objetivo principal gestionar la autenticación y autorización de usuarios dentro de una aplicación web. Define funciones para verificar si un usuario ha iniciado sesión, determinar su rol, y comprobar si tiene los permisos necesarios para acceder a ciertas funcionalidades o páginas. También incluye lógica para redirigir a los usuarios no autorizados.

**Descripción de Funciones y Clases:**

El archivo define las siguientes funciones:

*   **`verificar_sesion_activa()`**: Verifica si existe una sesión activa de usuario. Si no existe o el usuario no está autenticado (variables de sesión `loggedin` y `usuario_id` no configuradas correctamente), redirige al usuario a la página de inicio de sesión (`login.php`) con un mensaje de error.

*   **`obtener_rol_usuario()`**: Devuelve el rol del usuario almacenado en la sesión (`$_SESSION['rol_usuario']`). Si no se ha definido un rol, devuelve `null`.

*   **`es_admin()`, `es_tecnico()`, `es_auditor()`, `es_registrador()`**:  Funciones booleanas que verifican si el rol del usuario actual coincide con el rol especificado (admin, tecnico, auditor, registrador, respectivamente).  Internamente, todas llaman a `obtener_rol_usuario()`.

*   **`$GLOBALS['config_permisos_roles']`**: Un array asociativo global que define los permisos asignados a cada rol.  La clave del array es el rol (por ejemplo, 'admin', 'tecnico') y el valor es un array de strings representando los permisos que tiene asignado ese rol.

*   **`tiene_permiso_para($accion)`**: Verifica si el usuario actual tiene el permiso especificado (`$accion`).  Primero obtiene el rol del usuario y luego comprueba si el permiso dado está incluido en el array de permisos asignados a ese rol en `$config_permisos_roles`.

*   **`restringir_acceso_pagina($roles_o_permisos_permitidos = [])`**:  Esta es la función más compleja.  Verifica si el usuario actual tiene acceso a la página, basándose en una lista de roles o permisos permitidos.
    *   Primero, llama a `verificar_sesion_activa()` para asegurarse de que el usuario haya iniciado sesión.
    *   Si la lista de roles/permisos permitidos está vacía, la función simplemente retorna (acceso concedido).
    *   Determina si el array `$roles_o_permisos_permitidos` contiene roles o permisos, verificando el primer elemento.
    *   Si contiene roles, comprueba si el rol del usuario actual está en la lista de roles permitidos.
    *   Si contiene permisos, itera sobre la lista y usa `tiene_permiso_para()` para verificar si el usuario tiene *al menos uno* de los permisos requeridos.
    *   Si el acceso no está concedido, establece un mensaje de error en la sesión (`$_SESSION['error_acceso_pagina']`) y redirige al usuario a `menu.php`.

**Dependencias Clave:**

*   **`session_start()`**: La función al inicio del script inicia o reanuda una sesión PHP.  Esto es fundamental para el funcionamiento de la autenticación basada en sesiones.
*   **`$_SESSION`**:  La superglobal `$_SESSION` se utiliza para almacenar información sobre la sesión del usuario, como el estado de inicio de sesión (`loggedin`), el ID del usuario (`usuario_id`) y el rol del usuario (`rol_usuario`).
*   **`header()`**:  La función `header()` se utiliza para enviar encabezados HTTP. En este caso, se utiliza para redirigir a los usuarios a otras páginas (por ejemplo, `login.php` o `menu.php`) si no tienen los permisos necesarios o no han iniciado sesión.
*   **`exit;`**: Detiene la ejecución del script, normalmente después de una redirección, para asegurar que el usuario no pueda acceder al contenido protegido.
*   **`login.php`**:  Este script es el destino al que se redirige a los usuarios que no han iniciado sesión.
*   **`menu.php`**: Este script es el destino al que se redirige a los usuarios que no tienen permisos suficientes para acceder a una página.
```

---

## Archivo: `repo_temporal/backend/db.php`

```markdown
## Resumen del archivo `repo_temporal/backend/db.php`

**Propósito Principal:**

El archivo `db.php` tiene como propósito principal establecer una conexión a una base de datos MySQL utilizando la extensión `mysqli` de PHP.  Define las credenciales de conexión (host, usuario, contraseña y nombre de la base de datos) y crea un objeto de conexión.  Además, maneja errores de conexión y termina la ejecución del script si la conexión falla.

**Descripción de Funciones/Clases:**

*   No define funciones ni clases explícitamente.  En cambio, utiliza la clase `mysqli` predefinida en PHP.
*   **`$conn = new mysqli($host, $user, $pass, $db);`**:  Esta línea crea una nueva instancia de la clase `mysqli`, que representa la conexión a la base de datos.  Los parámetros son las variables de configuración previamente definidas.
*   **`$conn->connect_error`**: Esta propiedad de la instancia de `mysqli` almacena cualquier error que ocurra durante el intento de conexión.
*   **`die("Conexión fallida: " . $conn->connect_error);`**: Esta instrucción finaliza la ejecución del script y muestra un mensaje de error si la conexión a la base de datos falla.

**Dependencias Clave:**

*   **PHP:** El archivo es un script PHP, por lo que requiere un intérprete de PHP para ser ejecutado.
*   **`mysqli` extension:**  El código depende de la extensión `mysqli` de PHP para interactuar con la base de datos MySQL. Esta extensión debe estar habilitada en la configuración de PHP.
*   **MySQL database:** Necesita un servidor de base de datos MySQL en ejecución y accesible en el host especificado (`localhost` en este caso).
*   **Database credentials:**  Requiere las credenciales correctas (usuario, contraseña y nombre de la base de datos) para autenticarse en el servidor MySQL. Es importante notar que la contraseña está actualmente en blanco, lo cual podría ser un problema de seguridad si se usa en producción.
```

---

## Archivo: `repo_temporal/backend/historial_helper.php`

```markdown
## Resumen de `repo_temporal/backend/historial_helper.php`

**Propósito principal:**

El archivo `historial_helper.php` proporciona una función para registrar eventos relacionados con el historial de un activo en una base de datos. Su objetivo es centralizar la lógica para la gestión del historial de activos, permitiendo registrar cambios, traslados, bajas, y otras acciones relevantes, junto con información adicional como el usuario responsable y los datos antes y después del cambio.

**Descripción de funciones:**

*   **`registrar_evento_historial($conexion, $id_activo, $tipo_evento, $descripcion_evento, $usuario_responsable = null, $datos_anteriores_array = null, $datos_nuevos_array = null)`:**

    *   Esta función es el núcleo del archivo.  Recibe información sobre un evento ocurrido a un activo y lo registra en la tabla `historial_activos` de la base de datos.
    *   **Parámetros:**
        *   `$conexion`:  Un objeto de conexión `mysqli` a la base de datos.
        *   `$id_activo`: El ID del activo al que pertenece el evento.
        *   `$tipo_evento`: Una cadena que representa el tipo de evento (ej: 'CREACIÓN', 'ACTUALIZACIÓN', 'TRASLADO', 'BAJA'). Se espera que se utilicen las constantes definidas en el archivo.
        *   `$descripcion_evento`:  Una descripción legible por humanos del evento ocurrido.
        *   `$usuario_responsable`:  (Opcional) El nombre de usuario responsable de la acción.
        *   `$datos_anteriores_array`: (Opcional) Un array asociativo con los datos del activo *antes* del cambio.  Se convierte a JSON antes de ser almacenado.
        *   `$datos_nuevos_array`: (Opcional) Un array asociativo con los datos del activo *después* del cambio. Se convierte a JSON antes de ser almacenado.
    *   **Funcionalidad:**
        *   Convierte los arrays `$datos_anteriores_array` y `$datos_nuevos_array` a formato JSON utilizando `json_encode`. La opción `JSON_UNESCAPED_UNICODE` asegura que los caracteres Unicode se mantengan legibles.
        *   Prepara una consulta SQL parametrizada (prepared statement) para insertar los datos en la tabla `historial_activos`.
        *   Vincula los parámetros a la consulta SQL.
        *   Ejecuta la consulta.
        *   Maneja errores al preparar o ejecutar la consulta, registrándolos en el registro de errores del servidor utilizando `error_log`.
        *   Retorna `true` si el evento se registró correctamente, y `false` en caso de error.
        *   Cierra el statement (`$stmt->close()`) después de la ejecución para liberar recursos.

**Constantes Definidas:**

*   `HISTORIAL_TIPO_CREACION`: Define la constante para el tipo de evento "CREACIÓN".
*   `HISTORIAL_TIPO_ACTUALIZACION`: Define la constante para el tipo de evento "ACTUALIZACIÓN".
*   `HISTORIAL_TIPO_TRASLADO`: Define la constante para el tipo de evento "TRASLADO".
*   `HISTORIAL_TIPO_BAJA`: Define la constante para el tipo de evento "BAJA".
*   `HISTORIAL_TIPO_MANTENIMIENTO`: Comentada. Probablemente planeada para una funcionalidad futura relacionada con el mantenimiento de los activos.

**Dependencias Clave:**

*   **MySQLi:** La función depende de la extensión MySQLi de PHP para interactuar con la base de datos.  Requiere una conexión MySQLi activa (`$conexion`) para funcionar.
*   **JSON:** Utiliza las funciones `json_encode` y `JSON_UNESCAPED_UNICODE` para convertir arrays asociativos en cadenas JSON, lo que implica una dependencia de la extensión JSON de PHP.
*   **Tabla `historial_activos`:**  La función está diseñada para insertar datos en una tabla llamada `historial_activos`.  La estructura de esta tabla (columnas y tipos de datos) es una dependencia implícita.  Se espera que tenga al menos las columnas: `id_activo`, `tipo_evento`, `descripcion_evento`, `usuario_responsable`, `datos_anteriores`, `datos_nuevos`.
*   **Registro de errores del servidor:** Utiliza la función `error_log` para registrar errores.
```

---

