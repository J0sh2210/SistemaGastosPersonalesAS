--CREATE DATABASE SistemasGastosAS

--USE SistemasGastosAS;


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

--SP agregar movimiento y editar

USE SistemasGastosAS;
GO

-- 1. SP para Registrar un Ingreso (Fuerza el IdTipo = 1)
CREATE PROCEDURE sp_RegistrarIngreso
    @Concepto VARCHAR(30),
    @Monto DECIMAL(12,2),
    @IdCliente INT
AS
BEGIN
    DECLARE @NuevoId INT;
    
    INSERT INTO Movimiento (Concepto, Monto, FechaMovimiento, IdCliente, IdTipo)
    VALUES (@Concepto, @Monto, GETDATE(), @IdCliente, 1);
    
    SET @NuevoId = SCOPE_IDENTITY();
    
    -- Retornamos el registro recién creado para que la API lo devuelva
    SELECT IdMovimiento, Concepto, Monto, FechaMovimiento, IdCliente, IdTipo 
    FROM Movimiento 
    WHERE IdMovimiento = @NuevoId;
END;
GO

-- 2. SP para Editar un Ingreso (Asegurando que solo afecte a IdTipo = 1)
CREATE PROCEDURE sp_EditarIngreso
    @IdMovimiento INT,
    @Concepto VARCHAR(30),
    @Monto DECIMAL(12,2)
AS
BEGIN
    UPDATE Movimiento
    SET Concepto = @Concepto,
        Monto = @Monto
    WHERE IdMovimiento = @IdMovimiento AND IdTipo = 1;
    
    -- Retornamos el registro actualizado (si no existe o no era ingreso, no devuelve nada)
    SELECT IdMovimiento, Concepto, Monto, FechaMovimiento, IdCliente, IdTipo 
    FROM Movimiento 
    WHERE IdMovimiento = @IdMovimiento;
--Ver movimientos mes actual
USE SistemasGastosAS;
GO

CREATE PROCEDURE sp_ObtenerMovimientosMesActual
    @IdCliente INT
AS
BEGIN
    -- Selecciona los movimientos y hace un JOIN para traer el nombre del tipo (Ingreso/Egreso)
    SELECT 
        m.IdMovimiento,
        m.Concepto,
        m.Monto,
        m.FechaMovimiento,
        m.IdCliente,
        m.IdTipo,
        t.Nombre AS NombreTipoMovimiento
    FROM Movimiento m
    INNER JOIN TipoMovimiento t ON m.IdTipo = t.IdTipo
    WHERE m.IdCliente = @IdCliente
      -- Filtro estricto para el mes y año actuales
      AND MONTH(m.FechaMovimiento) = MONTH(GETDATE())
      AND YEAR(m.FechaMovimiento) = YEAR(GETDATE())
    ORDER BY m.FechaMovimiento DESC;
END;
GO

USE SistemasGastosAS;
GO

ALTER PROCEDURE sp_ObtenerMovimientosMesActual
    @IdCliente INT,
    @Mes INT,
    @Anio INT
AS
BEGIN
    SELECT 
        m.IdMovimiento,
        m.Concepto,
        m.Monto,
        m.FechaMovimiento,
        m.IdCliente,
        m.IdTipo,
        t.Nombre AS NombreTipoMovimiento
    FROM Movimiento m
    INNER JOIN TipoMovimiento t ON m.IdTipo = t.IdTipo
    WHERE m.IdCliente = @IdCliente
      AND MONTH(m.FechaMovimiento) = @Mes
      AND YEAR(m.FechaMovimiento) = @Anio
    ORDER BY m.FechaMovimiento DESC;
END;
GO
-- =============================================
-- SP Filtrar Movimientos por Mes
-- =============================================
CREATE PROCEDURE sp_FiltrarMovimientosPorMes
    @Mes   INT,
    @Anio  INT
AS
BEGIN
    SET NOCOUNT ON;

    IF @Mes < 1 OR @Mes > 12
        THROW 50001, 'El mes debe estar entre 1 y 12', 1;

    IF @Anio < 2000
        THROW 50002, 'El anio no es valido', 1;

    SELECT
        IdMovimiento,
        Concepto,
        Monto,
        FechaMovimiento,
        IdCliente,
        IdTipo
    FROM Movimiento
    WHERE MONTH(FechaMovimiento) = @Mes
      AND YEAR(FechaMovimiento) = @Anio
    ORDER BY FechaMovimiento DESC;
END

-- SP y tabla para metas de ahorro
Use SistemasGastosAS;
GO
CREATE TABLE MetasAhorro (
    IdMeta INT PRIMARY KEY IDENTITY(1,1),
    IdUsuario INT,
    NombreMeta VARCHAR(100),
    MontoObjetivo DECIMAL(12,2),
    FechaLimite DATE,
    MontoActual DECIMAL(12,2)
)

CREATE PROCEDURE sp_CrearMetaAhorro
    @IdUsuario INT,
    @NombreMeta VARCHAR(100),
    @MontoObjetivo DECIMAL(12,2),
    @FechaLimite DATE,
    @MontoActual DECIMAL(12,2)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY

        -- Validar que el monto objetivo sea mayor a cero
        IF @MontoObjetivo <= 0
        BEGIN
            THROW 50001, 'El monto objetivo debe ser mayor a cero.', 1;
        END

        -- Validar que la fecha limite no sea anterior a hoy
        IF @FechaLimite < CAST(GETDATE() AS DATE)
        BEGIN
            THROW 50002, 'La fecha limite no puede ser anterior a la fecha actual.', 1;
        END

        -- Validar que el monto actual no sea negativo
        IF @MontoActual < 0
        BEGIN
            THROW 50003, 'El monto actual no puede ser negativo.', 1;
        END

        -- Insertar la meta de ahorro
        INSERT INTO MetasAhorro
        (
            IdUsuario,
            NombreMeta,
            MontoObjetivo,
            FechaLimite,
            MontoActual
        )
        VALUES
        (
            @IdUsuario,
            @NombreMeta,
            @MontoObjetivo,
            @FechaLimite,
            @MontoActual
        );

        -- Retornar el Id generado
        SELECT SCOPE_IDENTITY() AS IdMeta;

    END TRY

    BEGIN CATCH

        -- Retornar error
        THROW;

    END CATCH

END;
GO

INSERT INTO MetasAhorro
(
    IdUsuario,
    NombreMeta,
    MontoObjetivo,
    FechaLimite,
    MontoActual
)
VALUES
(1, 'Viaje a Japón', 15000, '2026-12-31', 2000);

INSERT INTO MetasAhorro
(
    IdUsuario,
    NombreMeta,
    MontoObjetivo,
    FechaLimite,
    MontoActual
)
VALUES
(1, 'Comprar Laptop', 8000, '2026-08-15', 1500);

INSERT INTO MetasAhorro
(
    IdUsuario,
    NombreMeta,
    MontoObjetivo,
    FechaLimite,
    MontoActual
)
VALUES
(2, 'Fondo de Emergencia', 10000, '2027-01-01', 3000);

INSERT INTO MetasAhorro
(
    IdUsuario,
    NombreMeta,
    MontoObjetivo,
    FechaLimite,
    MontoActual
)
VALUES
(3, 'Comprar Moto', 25000, '2027-06-30', 5000);

