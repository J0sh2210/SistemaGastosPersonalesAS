CREATE DATABASE SistemasGastosAS;
GO
USE SistemasGastosAS;
GO

CREATE TABLE Cliente (
  IdCliente INT PRIMARY KEY IDENTITY(1,1),
  PrimerNombre VARCHAR(25),
  SegundoNombre VARCHAR(25),
  PrimerApellido VARCHAR(25),
  SegundoApellido VARCHAR(25),
  FechaCreacion DATETIME,
  Estado CHAR(1)
);

CREATE TABLE Correo (
  IdCorreo INT PRIMARY KEY IDENTITY(1,1),
  Correo VARCHAR(100) UNIQUE,
  IdCliente INT,
  CONSTRAINT Fk_Correo_Cliente FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente)
);

CREATE TABLE Telefono (
  IdTelefono INT PRIMARY KEY IDENTITY(1,1),
  Telefono VARCHAR(50) UNIQUE,
  IdCliente INT,
  CONSTRAINT Fk_Telefono_Cliente FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente)
);

CREATE TABLE CuentaUsuario (
  IdCuentaUsuario INT PRIMARY KEY IDENTITY(1,1),
  Contrase�a VARCHAR(100),
  NombreUsuario VARCHAR(25) UNIQUE,
  IdCliente INT,
  CONSTRAINT FK_CuentaUsuario_Cliente FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente)
);

CREATE TABLE TipoMovimiento (
  IdTipo INT PRIMARY KEY IDENTITY(1,1),
  Nombre VARCHAR(10),
  Naturaleza VARCHAR(10)
);

INSERT INTO TipoMovimiento (Nombre, Naturaleza) VALUES ('Ingreso', 'Credito');
INSERT INTO TipoMovimiento (Nombre, Naturaleza) VALUES ('Egreso', 'Debito');

CREATE TABLE Movimiento (
  IdMovimiento INT PRIMARY KEY IDENTITY(1,1),
  Concepto VARCHAR(30),
  Monto DECIMAL(12,2),
  FechaMovimiento DATETIME,
  IdCliente INT,
  IdTipo INT,
  CONSTRAINT FK_Movimiento_Cliente FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente),
  CONSTRAINT FK_Movimiento_Tipo FOREIGN KEY (IdTipo) REFERENCES TipoMovimiento(IdTipo)
);

go

CREATE TABLE GastoRecurrente (
  IdGastoRecurrente INT PRIMARY KEY IDENTITY(1,1),
  Concepto VARCHAR(100) NOT NULL,
  Monto DECIMAL(12,2) NOT NULL,
  FechaInicio DATETIME NOT NULL,
  Frecuencia VARCHAR(20) NOT NULL,
  IdCliente INT NOT NULL,
  CONSTRAINT FK_GastoRecurrente_Cliente FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente)
);

ALTER TABLE GastoRecurrente
ADD Activo BIT NOT NULL DEFAULT 1;

select * from GastoRecurrente