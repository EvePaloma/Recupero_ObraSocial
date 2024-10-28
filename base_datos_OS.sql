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
INSERT INTO obra_social (nombre, siglas, telefono, detalle, domicilio_central, domicilio_cp, cuit) VALUES
('Swiss Medical', 'SMG', '0810-333-8876', 'Obra social privada con cobertura integral.', 'Av. Pueyrredón 715, CABA', '1032', '30-65748512-1'),
('Galeno', 'GALENO', '0800-777-4253', 'Prestadora de servicios de salud privada.', 'Av. Córdoba 1455, CABA', '1055', '30-57694713-2'),
('OSDE Binario', 'OSDE', '0810-555-6733', 'Obra social privada con múltiples planes de cobertura.', 'Av. Leandro N. Alem 1067, CABA', '', '30-52765890-6'),
('Medicus', 'MEDICUS', '0800-333-6334', 'Obra social privada con cobertura en todo el país.', 'Av. Córdoba 1402, CABA', '1055', '30-64578932-7'),
('Omint', 'OMINT', '0810-666-6646', 'Cobertura médica privada con múltiples servicios.', 'Maipú 501, CABA', '', '30-58412378-4'),
('Sancor Salud', 'SANCOR', '0800-777-2363', 'Obra social privada orientada a brindar cobertura amplia.', 'Av. Rivadavia 1234, CABA', '1034', '30-67485913-8'),
('Osdepyme', 'OSDEPYME', '0810-122-0533', 'Obra social privada para pequeñas y medianas empresas.', 'Av. Rivadavia 4155, CABA', '', '30-57681234-0'),
('Avalian', 'AVALIAN', '0800-444-7007', 'Obra social privada con cobertura nacional.', 'Cerrito 550, CABA', '', '30-58971356-1');

select * from obra_social;
INSERT INTO afip (nombre) VALUES 
('Entidad de la Seguridad Social'), 
('Entidad con Código de Obra Social'), 
('Entidad Prestadora de Servicios de Salud');

INSERT INTO tratamiento (codigo, nombre, precio, fecha_precio, siglas, descripcion) VALUES 
('1001', 'Sutura Simple', 1800.00, '2024-01-10', 'SS', 'Cierre de heridas superficiales con suturas en urgencias.'),
('1002A', 'Sutura Compleja', 3400.00, '2024-01-11', 'SC', 'Sutura para heridas profundas o con múltiples capas de tejido.'),
('1010', 'Escayola Brazo', 2800.00, '2024-01-12', 'EB', 'Inmovilización de brazo con escayola debido a fracturas.'),
('102B', 'Escayola Pierna', 3500.00, '2024-01-12', 'EP', 'Inmovilización de pierna en caso de fractura o esguince severo.'),
('103', 'Vendaje Compresivo', 700.00, '2024-01-13', 'VC', 'Vendaje para control de sangrado o soporte de lesiones.'),
('104X', 'Lavado de Estómago', 4500.00, '2024-01-14', 'LE', 'Procedimiento para remover sustancias tóxicas ingeridas.'),
('105', 'Administración Oxígeno', 1500.00, '2024-01-15', 'AO', 'Suministro de oxígeno en casos de insuficiencia respiratoria.'),
('106N', 'Nebulización', 1000.00, '2024-01-16', 'NB', 'Terapia respiratoria para pacientes con asma o dificultad respiratoria.'),
('107', 'Inyección Intravenosa', 800.00, '2024-01-17', 'IV', 'Administración intravenosa de medicamentos de urgencia.'),
('108Y', 'Inyección Intramuscular', 700.00, '2024-01-18', 'IM', 'Aplicación de medicamentos en el músculo para rápida absorción.'),
('109', 'Curación Simple', 900.00, '2024-01-19', 'CS', 'Limpieza y cuidado de heridas leves.'),
('110F', 'Curación Compleja', 1800.00, '2024-01-20', 'CC', 'Curación de heridas complejas o infectadas en urgencias.'),
('111', 'Aspiración de Vías Aéreas', 2500.00, '2024-01-21', 'AVA', 'Retiro de secreciones en vías respiratorias en caso de obstrucción.'),
('112G', 'Reanimación Cardiopulmonar', 12000.00, '2024-01-22', 'RCP', 'Procedimiento de emergencia para restaurar la respiración y circulación.'),
('113', 'Extracción de Cuerpo Extraño', 3500.00, '2024-01-23', 'ECE', 'Extracción de cuerpos extraños en nariz, garganta u ojos.'),
('114Z', 'Tratamiento de Quemaduras', 2200.00, '2024-01-24', 'TQ', 'Aplicación de enfriamiento para quemaduras superficiales.'),
('115', 'Estabilización de Fractura', 4000.00, '2024-01-25', 'EF', 'Inmovilización y estabilización inicial de fracturas.'),
('116A', 'Sutura de Cejas', 2300.00, '2024-01-26', 'SCJ', 'Cierre de heridas en la zona de cejas con sutura estética.'),
('117', 'Administración de Suero', 1300.00, '2024-01-27', 'AS', 'Suministro intravenoso de líquidos y electrolitos.'),
('118B', 'Analgesia Controlada', 1800.00, '2024-01-28', 'AC', 'Aplicación de analgésicos para control de dolor en urgencias.');

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
