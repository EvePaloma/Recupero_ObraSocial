DROP DATABASE IF EXISTS `recupero_obra_social`;
CREATE DATABASE `recupero_obra_social`;
USE recupero_obra_social;
DROP TABLE IF EXISTS `estado`;
CREATE TABLE `estado` (
  `id_estado` int NOT NULL,
  `nombre` varchar(20) NOT NULL,
  PRIMARY KEY (`id_estado`)
);
insert into estado(id_estado, nombre) values (0, "INACTIVO"), (1, "ACTIVO");
DROP TABLE IF EXISTS `tipo_documento`;
CREATE TABLE `tipo_documento` (
  `id_tipo_documento` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) NOT NULL,
  PRIMARY KEY (`id_tipo_documento`)
);
INSERT INTO tipo_documento (nombre) 
VALUES ('DNI'),('Pasaporte');
DROP TABLE IF EXISTS `rol`;
CREATE TABLE `rol` (
  `id_rol` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) NOT NULL,
  PRIMARY KEY (`id_rol`)
);
DROP TABLE IF EXISTS `tipo_matricula`;
CREATE TABLE `tipo_matricula` (
  `id_tipo_matricula` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(10) NOT NULL,
  PRIMARY KEY (`id_tipo_matricula`)
);
DROP TABLE IF EXISTS `afip`;
CREATE TABLE `afip` (
  `id_afip` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  PRIMARY KEY (`id_afip`),
  UNIQUE KEY `nombre_UNIQUE` (`nombre`)
);
DROP TABLE IF EXISTS `pais`;
CREATE TABLE `pais` (
  `id_pais` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) NOT NULL,
  PRIMARY KEY (`id_pais`)
);
DROP TABLE IF EXISTS `ciudad`;
CREATE TABLE `ciudad` (
  `id_ciudad` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `id_pais` int NOT NULL,
  PRIMARY KEY (`id_ciudad`),
  FOREIGN KEY (`id_pais`) REFERENCES `pais` (`id_pais`)
);
DROP TABLE IF EXISTS `barrio`;
CREATE TABLE `barrio` (
  `id_barrio` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(25) NOT NULL,
  `id_ciudad` int NOT NULL,
  PRIMARY KEY (`id_barrio`),
  FOREIGN KEY (`id_ciudad`) REFERENCES `ciudad` (`id_ciudad`)
);

DROP TABLE IF EXISTS `especialidad`;
CREATE TABLE `especialidad` (
  `id_especialidad` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(40) NOT NULL,
  `activo` tinyint NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_especialidad`)
);
DROP TABLE IF EXISTS `medico`;
CREATE TABLE `medico` (
  `id_medico` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `apellido` varchar(45) NOT NULL,
  `matricula` varchar(20) NOT NULL,
  `telefono` varchar(45) NOT NULL,
  `documento` varchar(45) NOT NULL,
  `activo` tinyint NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_medico`),
  UNIQUE KEY `documento_UNIQUE` (`documento`)
);

DROP TABLE IF EXISTS `obra_social`;
CREATE TABLE `obra_social` (
  `id_obra_social` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `siglas` varchar(20) NOT NULL,
  `telefono` varchar(45) NOT NULL,
  `detalle` longtext,
  `domicilio_central` varchar(45) DEFAULT NULL,
  `domicilio_cp` varchar(45) DEFAULT NULL,
  `cuit` varchar(30) NOT NULL,
  `id_afip` int DEFAULT NULL,
  `activo` tinyint NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_obra_social`),
  UNIQUE KEY `id_obra_social_UNIQUE` (`id_obra_social`),
  FOREIGN KEY (`id_afip`) REFERENCES `afip` (`id_afip`)
);

DROP TABLE IF EXISTS `paciente`;
CREATE TABLE `paciente` (
  `id_paciente` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `apellido` varchar(45) NOT NULL,
  `nacimiento` date NOT NULL,
  `tipo_documento` int NOT NULL,
  `documento` varchar(45) NOT NULL,
  `id_obra_social` int NOT NULL,
  `nro_afiliado` varchar(45) NOT NULL,
  `activo` tinyint NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_paciente`),
  FOREIGN KEY (`tipo_documento`) REFERENCES `tipo_documento` (`id_tipo_documento`),
  FOREIGN KEY (`id_obra_social`) REFERENCES `obra_social` (`id_obra_social`)
);
DROP TABLE IF EXISTS `detalle_obra_social`;
CREATE TABLE `detalle_obra_social` (
  `id_detalle_os` int NOT NULL AUTO_INCREMENT,
  `id_paciente` int NOT NULL,
  `id_obra_social` int NOT NULL,
  `nro_afiliado` varchar(25) NOT NULL,
  `caracter` varchar(25) NOT NULL,
  `activo` tinyint NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_detalle_os`),
  FOREIGN KEY (`id_paciente`) REFERENCES `paciente` (`id_paciente`),
  FOREIGN KEY (`id_obra_social`) REFERENCES `obra_social` (`id_obra_social`)
);

DROP TABLE IF EXISTS `tratamiento`;
CREATE TABLE `tratamiento` (
  `id_tratamiento` int NOT NULL AUTO_INCREMENT,
  `codigo` varchar(15) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `precio` float NOT NULL,
  `fecha_precio` date NOT NULL,
  `siglas` varchar(20) NOT NULL,
  `descripcion` longtext,
  `activo` tinyint NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_tratamiento`)
);

DROP TABLE IF EXISTS `usuario`;
CREATE TABLE `usuario` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `apellido` varchar(45) NOT NULL,
  `documento` varchar(45) NOT NULL,
  `telefono` varchar(45),
  `clave` varchar(20) NOT NULL,
  `activo` tinyint NOT NULL DEFAULT 1,
  `id_rol` int NOT NULL DEFAULT 2,
  PRIMARY KEY (`id_usuario`),
  FOREIGN KEY (`id_rol`) REFERENCES `rol` (`id_rol`)
);

DROP TABLE IF EXISTS `ficha`;
CREATE TABLE `ficha` (
  `id_ficha` int NOT NULL AUTO_INCREMENT,
  `id_paciente` int NOT NULL,
  `id_obra_social` int NOT NULL,
  `id_medico` int NOT NULL,
  `fecha` date NOT NULL,
  `total` float NOT NULL,
  `activo` tinyint NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_ficha`),
  FOREIGN KEY (`id_paciente`) REFERENCES `paciente` (`id_paciente`),
  FOREIGN KEY (`id_obra_social`) REFERENCES `obra_social` (`id_obra_social`),
  FOREIGN KEY (`id_medico`) REFERENCES `medico` (`id_medico`)
);

DROP TABLE IF EXISTS `detalle_ficha`;
CREATE TABLE `detalle_ficha` (
  `id_detalle` int NOT NULL AUTO_INCREMENT,
  `id_ficha` int NOT NULL,
  `id_tratamiento` int NOT NULL,
  `cantidad` int NOT NULL DEFAULT 1 ,
  `precio_unitario` float NOT NULL,
  `subtotal` float AS (cantidad * precio_unitario) STORED,
  `activo` tinyint NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_detalle`),
  FOREIGN KEY (`id_ficha`) REFERENCES `ficha` (`id_ficha`),
  FOREIGN KEY (`id_tratamiento`) REFERENCES `tratamiento` (`id_tratamiento`)
);

---------------------------------------------------------------------------
---insertar datos---
insert into rol(nombre) values ("ADMINISTRADOR"),("USUARIO");
insert into usuario (nombre, apellido, documento, telefono, clave, id_rol) values ("LUCRECIA", "SALAZAR", "4563255", "3562455", "623", 1);

from * from USUARIO;

use recupero_obra_social;
INSERT INTO obra_social (nombre, siglas, telefono, detalle, domicilio_central, domicilio_cp, cuit, id_afip) VALUES
('SWISS MEDICAL', 'SMG', '08103338876', 'OBRA SOCIAL PRIVADA CON COBERTURA INTEGRAL.', 'AV. PUEYRREDÓN 715, CABA', '1032', '30657485121', 1),
('GALENO', 'GALENO', '08007774253', 'PRESTADORA DE SERVICIOS DE SALUD PRIVADA.', 'AV. CÓRDOBA 1455, CABA', '1055', '30576947132', 2),
('OSDE BINARIO', 'OSDE', '08105556733', 'OBRA SOCIAL PRIVADA CON MÚLTIPLES PLANES DE COBERTURA.', 'AV. LEANDRO N. ALEM 1067, CABA', '', '30527658906', 3),
('MEDICUS', 'MEDICUS', '08003336334', 'OBRA SOCIAL PRIVADA CON COBERTURA EN TODO EL PAÍS.', 'AV. CÓRDOBA 1402, CABA', '1055', '30645789327', 1),
('OMINT', 'OMINT', '08106666646', 'COBERTURA MÉDICA PRIVADA CON MÚLTIPLES SERVICIOS.', 'MAIPÚ 501, CABA', '', '30584123784', 2),
('SANCOR SALUD', 'SANCOR', '08007772363', 'OBRA SOCIAL PRIVADA ORIENTADA A BRINDAR COBERTURA AMPLIA.', 'AV. RIVADAVIA 1234, CABA', '1034', '30674859138', 3),
('OSDEPYME', 'OSDEPYME', '08101220533', 'OBRA SOCIAL PRIVADA PARA PEQUEÑAS Y MEDIANAS EMPRESAS.', 'AV. RIVADAVIA 4155, CABA', '', '30576812340', 1),
('AVALIAN', 'AVALIAN', '08004447007', 'OBRA SOCIAL PRIVADA CON COBERTURA NACIONAL.', 'CERRITO 550, CABA', '', '30589713561', 2),
('PREMEDIC', 'PREMEDIC', '08001234567', 'OBRA SOCIAL PRIVADA CON COBERTURA REGIONAL.', 'AV. SANTA FE 1234, CABA', '1045', '30678912345', 3),
('HOSPITAL BRITÁNICO', 'HB', '08005551234', 'OBRA SOCIAL PRIVADA CON SERVICIOS DE ALTA COMPLEJIDAD.', 'AV. INDEPENDENCIA 1234, CABA', '1100', '30567891234', 1),
('ITALMED', 'ITALMED', '08007778899', 'OBRA SOCIAL PRIVADA CON COBERTURA INTERNACIONAL.', 'AV. ITALIA 1234, CABA', '1200', '30678945612', 2),
('CEMIC', 'CEMIC', '08006667777', 'OBRA SOCIAL PRIVADA CON SERVICIOS DE ALTA CALIDAD.', 'AV. LAS HERAS 1234, CABA', '1300', '30567894561', 3),
('OSPAT', 'OSPAT', '08001112233', 'OBRA SOCIAL DEL PERSONAL DE LA ACTIVIDAD DEL TURF.', 'AV. SAN JUAN 1234, CABA', '1400', '30678912346', 1),
('OSMATA', 'OSMATA', '08002223344', 'OBRA SOCIAL DE MAESTRANZA Y SERVICIOS.', 'AV. BELGRANO 1234, CABA', '1500', '30567891235', 2),
('OSUTHGRA', 'OSUTHGRA', '08003334455', 'OBRA SOCIAL DE LA UNION DE TRABAJADORES HOTELEROS Y GASTRONOMICOS.', 'AV. CORRIENTES 1234, CABA', '1600', '30678912347', 3),
('OSPE', 'OSPE', '08004445566', 'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA DEL CUERO.', 'AV. ENTRE RIOS 1234, CABA', '1700', '30567891236', 1),
('OSPACP', 'OSPACP', '08005556677', 'OBRA SOCIAL DEL PERSONAL DE LA ACTIVIDAD DEL PLASTICO.', 'AV. CALLAO 1234, CABA', '1800', '30678912348', 2);

select * from obra_social;
INSERT INTO afip (nombre) VALUES 
('Entidad de la Seguridad Social'), 
('Entidad con Código de Obra Social'), 
('Entidad Prestadora de Servicios de Salud');

INSERT INTO tratamiento (codigo, nombre, precio, fecha_precio, siglas, descripcion) VALUES 
('1001', 'SUTURA SIMPLE', 1800.00, '2024-01-10', 'SS', 'CIERRE DE HERIDAS SUPERFICIALES CON SUTURAS EN URGENCIAS.'),
('1002A', 'SUTURA COMPLEJA', 3400.00, '2024-01-11', 'SC', 'SUTURA PARA HERIDAS PROFUNDAS O CON MÚLTIPLES CAPAS DE TEJIDO.'),
('1010', 'ESCAYOLA BRAZO', 2800.00, '2024-01-12', 'EB', 'INMOVILIZACIÓN DE BRAZO CON ESCAYOLA DEBIDO A FRACTURAS.'),
('102B', 'ESCAYOLA PIERNA', 3500.00, '2024-01-12', 'EP', 'INMOVILIZACIÓN DE PIERNA EN CASO DE FRACTURA O ESGUINCE SEVERO.'),
('103', 'VENDAJE COMPRESIVO', 700.00, '2024-01-13', 'VC', 'VENDAJE PARA CONTROL DE SANGRADO O SOPORTE DE LESIONES.'),
('104X', 'LAVADO DE ESTÓMAGO', 4500.00, '2024-01-14', 'LE', 'PROCEDIMIENTO PARA REMOVER SUSTANCIAS TÓXICAS INGERIDAS.'),
('105', 'ADMINISTRACIÓN OXÍGENO', 1500.00, '2024-01-15', 'AO', 'SUMINISTRO DE OXÍGENO EN CASOS DE INSUFICIENCIA RESPIRATORIA.'),
('106N', 'NEBULIZACIÓN', 1000.00, '2024-01-16', 'NB', 'TERAPIA RESPIRATORIA PARA PACIENTES CON ASMA O DIFICULTAD RESPIRATORIA.'),
('107', 'INYECCIÓN INTRAVENOSA', 800.00, '2024-01-17', 'IV', 'ADMINISTRACIÓN INTRAVENOSA DE MEDICAMENTOS DE URGENCIA.'),
('108Y', 'INYECCIÓN INTRAMUSCULAR', 700.00, '2024-01-18', 'IM', 'APLICACIÓN DE MEDICAMENTOS EN EL MÚSCULO PARA RÁPIDA ABSORCIÓN.'),
('109', 'CURACIÓN SIMPLE', 900.00, '2024-01-19', 'CS', 'LIMPIEZA Y CUIDADO DE HERIDAS LEVES.'),
('110F', 'CURACIÓN COMPLEJA', 1800.00, '2024-01-20', 'CC', 'CURACIÓN DE HERIDAS COMPLEJAS O INFECTADAS EN URGENCIAS.'),
('111', 'ASPIRACIÓN DE VÍAS AÉREAS', 2500.00, '2024-01-21', 'AVA', 'RETIRO DE SECRECIONES EN VÍAS RESPIRATORIAS EN CASO DE OBSTRUCCIÓN.'),
('112G', 'REANIMACIÓN CARDIOPULMONAR', 12000.00, '2024-01-22', 'RCP', 'PROCEDIMIENTO DE EMERGENCIA PARA RESTAURAR LA RESPIRACIÓN Y CIRCULACIÓN.'),
('113', 'EXTRACCIÓN DE CUERPO EXTRAÑO', 3500.00, '2024-01-23', 'ECE', 'EXTRACCIÓN DE CUERPOS EXTRAÑOS EN NARIZ, GARGANTA U OJOS.'),
('114Z', 'TRATAMIENTO DE QUEMADURAS', 2200.00, '2024-01-24', 'TQ', 'APLICACIÓN DE ENFRIAMIENTO PARA QUEMADURAS SUPERFICIALES.'),
('115', 'ESTABILIZACIÓN DE FRACTURA', 4000.00, '2024-01-25', 'EF', 'INMOVILIZACIÓN Y ESTABILIZACIÓN INICIAL DE FRACTURAS.'),
('116A', 'SUTURA DE CEJAS', 2300.00, '2024-01-26', 'SCJ', 'CIERRE DE HERIDAS EN LA ZONA DE CEJAS CON SUTURA ESTÉTICA.'),
('117', 'ADMINISTRACIÓN DE SUERO', 1300.00, '2024-01-27', 'AS', 'SUMINISTRO INTRAVENOSO DE LÍQUIDOS Y ELECTROLITOS.'),
('118B', 'ANALGESIA CONTROLADA', 1800.00, '2024-01-28', 'AC', 'APLICACIÓN DE ANALGÉSICOS PARA CONTROL DE DOLOR EN URGENCIAS.');

use recupero_obra_social;

INSERT INTO paciente (`nombre`, `apellido`, `nacimiento`, `tipo_documento`, `documento`, `id_obra_social`, `nro_afiliado`, `activo`)
VALUES 
  ('Juan', 'Pérez', '1985-03-15', 1, '12345678', 1, 'A123456', 1),
  ('María', 'Gómez', '1990-07-22', 2, '87654321', 2, 'B234567', 1),
  ('Carlos', 'Martínez', '1982-01-30', 1, '11223344', 3, 'C345678', 1),
  ('Ana', 'López', '1995-09-12', 2, '22334455', 4, 'D456789', 1),
  ('Pedro', 'Fernández', '1978-11-05', 1, '33445566', 5, 'E567890', 1),
  ('Lucía', 'Ramírez', '2001-04-18', 2, '44556677', 1, 'F678901', 1),
  ('Marta', 'Sánchez', '1993-06-25', 1, '55667788', 2, 'G789012', 1),
  ('José', 'Torres', '1988-10-29', 1, '66778899', 4, 'H890123', 1);
select * from paciente;
INSERT INTO `medico` (`nombre`, `apellido`, `matricula`, `telefono`, `documento`, `activo`)
VALUES 
  ('Laura', 'Pérez', '123456', '1234567890', '30123456', 1),
  ('Jorge', 'González', '234567', '0987654321', '30234567', 1),
  ('Ana', 'Martínez', '345678', '1122334455', '30345678', 1),
  ('Carlos', 'Ramírez', '456789', '5566778899', '30456789', 1),
  ('Marta', 'Díaz', '567890', '6677889900', '30567890', 1),
  ('José', 'Fernández', '678901', '7788990011', '30678901', 1),
  ('María', 'García', '789012', '8899001122', '30789012', 1),
  ('Luis', 'Torres', '890123', '9900112233', '30890123', 1),
  ('Raúl', 'Suárez', '901234', '1011121314', '30901234', 1),
  ('Carmen', 'López', '123457', '1213141516', '30012345', 1);
select * from medico;

SELECT * from ficha;
select * from detalle_ficha;
select * from tratamiento;
