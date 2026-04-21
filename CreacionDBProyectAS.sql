CREATE DATABASE SistemasGastosAS
--USE SistemasGastosAS


CREATE TABLE Cliente (
IdCliente INT PRIMARY KEY IDENTITY(1,1),
PrimerNombre VARCHAR(25),
SegundoNombre VARCHAR(25),
PrimerApellido VARCHAR(25),
SegundoApellido VARCHAR(25),
FechaCreacion DATETIME,
Estado CHAR(1)


)
CREATE TABLE Correo (
IdCorreo INT PRIMARY KEY IDENTITY(1,1),
Correo VARCHAR UNIQUE,
IdCliente INT
CONSTRAINT Fk_Correo_Cliente FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente)
)

CREATE TABLE Telefono (
IdTelefono INT PRIMARY KEY IDENTITY(1,1),
Telefono VARCHAR UNIQUE,
IdCliente INT
CONSTRAINT Fk_Telefono_Cliente FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente)
)





CREATE TABLE CuentaUsuario (
IdCuentaUsuario INT PRIMARY KEY IDENTITY(1,1),
Contrase�a VARCHAR(100),
NombreUsuario VARCHAR(25) UNIQUE,
IdCliente INT
CONSTRAINT
FK_CuentaUsuario_Cliente FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente)
)
CREATE TABLE TipoMovimiento (
IdTipo INT PRIMARY KEY IDENTITY(1,1),
Nombre VARCHAR(10),
Naturaleza VARCHAR(10)
)

INSERT INTO TipoMovimiento (Nombre, Naturaleza) VALUES ('Ingreso', 'Credito')
INSERT INTO TipoMovimiento (Nombre, Naturaleza) VALUES ('Egreso', 'Debito')

CREATE TABLE Movimiento (
IdMovimiento INT PRIMARY KEY IDENTITY(1,1),
Concepto VARCHAR(30),
Monto DECIMAL(12,2),
FechaMovimiento DATETIME,
IdCliente INT,
IdTipo INT

CONSTRAINT FK_Movimiento_Cliente FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente),
CONSTRAINT FK_Movimiento_Tipo FOREIGN KEY (IdTipo) REFERENCES TipoMovimiento(IdTipo)
)

CREATE TABLE TipoCategoriaMovimiento (
    IdTipoCategoria INT PRIMARY KEY IDENTITY(1,1),
    NombreTipo VARCHAR(30), 
    Descripcion VARCHAR(100)
)
INSERT INTO TipoCategoriaMovimiento (NombreTipo, Descripcion)
VALUES ('Fijo', 'Gastos fijos'), ('Variable', 'Gastos variables'),('Hormiga', 'Peque�os gastos'),('Inversion', 'Inversiones')

CREATE TABLE CategoriaMovimiento (
    IdCategoria INT PRIMARY KEY IDENTITY (1,1),
    NombreCategoria VARCHAR(50),
    IdTipoMovimiento INT, 
    IdTipoCategoria INT,  
    CONSTRAINT FK_Categoria_TipoMovimiento FOREIGN KEY (IdTipoMovimiento) REFERENCES TipoMovimiento(IdTipo),
    CONSTRAINT FK_Categoria_TipoCategoriaMovimiento FOREIGN KEY (IdTipoCategoria) REFERENCES TipoCategoriaMovimiento(IdTipoCategoria)
)

INSERT INTO CategoriaMovimiento (NombreCategoria, IdTipoMovimiento, IdTipoCategoria) VALUES ('Servicio', 2, 1)

INSERT INTO CategoriaMovimiento (NombreCategoria, IdTipoMovimiento, IdTipoCategoria) VALUES ('Alimentaci�n', 2, 3)

INSERT INTO CategoriaMovimiento (NombreCategoria, IdTipoMovimiento, IdTipoCategoria) VALUES ('Transporte', 2, 3)

INSERT INTO CategoriaMovimiento (NombreCategoria, IdTipoMovimiento, IdTipoCategoria) VALUES ('Entretenimiento', 2, 2)

INSERT INTO CategoriaMovimiento (NombreCategoria, IdTipoMovimiento, IdTipoCategoria) VALUES ('Ahorro', 1, 4)

ALTER TABLE Movimiento
ADD IdCategoria INT

ALTER TABLE Movimiento
ADD CONSTRAINT FK_Movimiento_Categoria
FOREIGN KEY (IdCategoria) REFERENCES CategoriaMovimiento(IdCategoria)

CREATE TABLE Bitacora (
    IdBitacora INT IDENTITY(1,1) PRIMARY KEY,
    Accion VARCHAR(50),
    Descripcion VARCHAR(255),
    Fecha DATETIME DEFAULT GETDATE()
)