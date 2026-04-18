USE master;
DROP DATABASE IF EXISTS SistemasGastosAS;
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
  FechaCreacion DATETIME DEFAULT GETDATE(),
  Estado CHAR(1)
);
GO

CREATE TABLE CuentaUsuario (
  IdCuentaUsuario INT PRIMARY KEY IDENTITY(1,1),
  NombreUsuario VARCHAR(25) UNIQUE,
  Contraseña VARCHAR(100),
  IdCliente INT,
  CONSTRAINT FK_CuentaUsuario_Cliente FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente)
);
GO

CREATE TABLE Correo (
  IdCorreo INT PRIMARY KEY IDENTITY(1,1),
  Correo VARCHAR(100) UNIQUE,
  IdCliente INT,
  CONSTRAINT Fk_Correo_Cliente FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente)
);
GO

CREATE TABLE Telefono (
  IdTelefono INT PRIMARY KEY IDENTITY(1,1),
  Telefono VARCHAR(20) UNIQUE,
  IdCliente INT,
  CONSTRAINT Fk_Telefono_Cliente FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente)
);
GO

CREATE TABLE TipoMovimiento (
  IdTipo INT PRIMARY KEY IDENTITY(1,1),
  Nombre VARCHAR(10),
  Naturaleza VARCHAR(10)
);
GO

INSERT INTO TipoMovimiento (Nombre, Naturaleza) VALUES ('Ingreso', 'Credito');
INSERT INTO TipoMovimiento (Nombre, Naturaleza) VALUES ('Egreso', 'Debito');
GO

CREATE TABLE Movimiento (
  IdMovimiento INT PRIMARY KEY IDENTITY(1,1),
  Concepto VARCHAR(30),
  Monto DECIMAL(12,2),
  FechaMovimiento DATETIME DEFAULT GETDATE(),
  IdCliente INT,
  IdTipo INT,
  CONSTRAINT FK_Movimiento_Cliente FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente),
  CONSTRAINT FK_Movimiento_Tipo FOREIGN KEY (IdTipo) REFERENCES TipoMovimiento(IdTipo)
);
GO

PRINT 'Database SistemasGastosAS created successfully!';

