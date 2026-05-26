--CREATE DATABASE SistemasGastosAS

--USE SistemasGastosAS;

--------------------------------------
        --CREACION DE TABLAS
--------------------------------------
-- TABLA 1
CREATE TABLE Cliente (
  IdCliente INT PRIMARY KEY IDENTITY(1,1),
  PrimerNombre VARCHAR(25),
  SegundoNombre VARCHAR(25),
  PrimerApellido VARCHAR(25),
  SegundoApellido VARCHAR(25),
  FechaCreacion DATETIME,
  Estado CHAR(1)
);
-- TABLA 2
CREATE TABLE Correo (
  IdCorreo INT PRIMARY KEY IDENTITY(1,1),
  Correo VARCHAR(100) UNIQUE,
  IdCliente INT,
  CONSTRAINT Fk_Correo_Cliente FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente)
);
-- TABLA 3
CREATE TABLE Telefono (
  IdTelefono INT PRIMARY KEY IDENTITY(1,1),
  Telefono VARCHAR(50) UNIQUE,
  IdCliente INT,
  CONSTRAINT Fk_Telefono_Cliente FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente)
);
-- TABLA 4
CREATE TABLE CuentaUsuario (
  IdCuentaUsuario INT PRIMARY KEY IDENTITY(1,1),
  Contrasena VARCHAR(100),
  NombreUsuario VARCHAR(25) UNIQUE,
  IdCliente INT,
  CONSTRAINT FK_CuentaUsuario_Cliente FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente)
);
-- TABLA 5
CREATE TABLE TipoMovimiento (
  IdTipo INT PRIMARY KEY IDENTITY(1,1),
  Nombre VARCHAR(10),
  Naturaleza VARCHAR(10)
);

-- TABLA 6
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
-- TABLA 7
CREATE TABLE TipoCategoriaMovimiento (
    IdTipoCategoria INT PRIMARY KEY IDENTITY(1,1),
    NombreTipo VARCHAR(50),
    Descripcion VARCHAR(100)
);
-- TABLA 8
CREATE TABLE CategoriaMovimiento (
    IdCategoria INT PRIMARY KEY IDENTITY(1,1),
    NombreCategoria VARCHAR(50) NOT NULL,
    IdTipoMovimiento INT NOT NULL,
    IdTipoCategoria INT NOT NULL,
    CONSTRAINT FK_CategoriaMovimiento_TipoMovimiento FOREIGN KEY (IdTipoMovimiento) REFERENCES TipoMovimiento(IdTipo),
    CONSTRAINT FK_CategoriaMovimiento_TipoCategoria FOREIGN KEY (IdTipoCategoria) REFERENCES TipoCategoriaMovimiento(IdTipoCategoria)
);

ALTER TABLE Movimiento ADD IdCategoria INT;
ALTER TABLE Movimiento ADD CONSTRAINT FK_Movimiento_Categoria
FOREIGN KEY (IdCategoria) REFERENCES CategoriaMovimiento(IdCategoria);
-- TABLA 9
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
-- TABLA 10
CREATE TABLE MetasAhorro (
    IdMeta INT PRIMARY KEY IDENTITY(1,1),
    IdUsuario INT,
    NombreMeta VARCHAR(100),
    MontoObjetivo DECIMAL(12,2),
    FechaLimite DATE,
    MontoActual DECIMAL(12,2)
)

-- TABLA 11
CREATE TABLE PresupuestoMensual (
    IdPresupuesto INT PRIMARY KEY IDENTITY(1,1),
    MontoPresupuesto DECIMAL(12,2) NOT NULL,
    IdCategoria INT NULL,
    MesAplicacion VARCHAR(20) NOT NULL,
    IdUsuario INT NOT NULL,

    FOREIGN KEY (IdUsuario) REFERENCES Cliente(IdCliente),
    FOREIGN KEY (IdCategoria) REFERENCES CategoriaMovimiento(IdCategoria)
);
ALTER TABLE PresupuestoMensual ADD PorcentajeAlerta DECIMAL(5,2) NOT NULL DEFAULT 80;
-- TABLA 12
CREATE TABLE Alerta (
    IdAlerta INT PRIMARY KEY IDENTITY(1,1),
    IdUsuario INT NOT NULL,
    IdCategoria INT NOT NULL,
    TipoAlerta VARCHAR(20),
    Mensaje VARCHAR(200),
    Gastado DECIMAL(12,2),
    LimitePresupuesto DECIMAL(12,2),
    Porcentaje DECIMAL(5,2),
    Mes INT,
    Anio INT,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_Alerta_Usuario FOREIGN KEY (IdUsuario) REFERENCES Cliente(IdCliente),
    CONSTRAINT FK_Alerta_Categoria FOREIGN KEY (IdCategoria) REFERENCES CategoriaMovimiento(IdCategoria)
);

------------------------------------------------------------
            --INSERCION DE DATOS INICIALES
------------------------------------------------------------
-- CLIENTE
INSERT INTO Cliente (PrimerNombre, SegundoNombre, PrimerApellido, SegundoApellido, FechaCreacion, Estado)
VALUES 
('Juan', 'Carlos', 'Pérez', 'Lopez', GETDATE(), 'A'),
('Maria', 'Fernanda', 'Gomez', 'Ruiz', GETDATE(), 'A'),
('Luis', 'Alberto', 'Martinez', 'Diaz', GETDATE(), 'A');

-- TIPO MOVIMIENTO
INSERT INTO TipoMovimiento (Nombre, Naturaleza)
VALUES 
('Ingreso', 'Credito'),
('Egreso', 'Debito');

-- TIPO CATEGORIA MOVIMIENTO
INSERT INTO TipoCategoriaMovimiento (NombreTipo, Descripcion)
VALUES 
('Fijo', 'Gastos fijos mensuales'),
('Variable', 'Gastos variables'),
('Hormiga', 'Pequeños gastos diarios'),
('Inversion', 'Dinero destinado a inversión');

-- CATEGORIA MOVIMIENTO
INSERT INTO CategoriaMovimiento (NombreCategoria, IdTipoMovimiento, IdTipoCategoria)
VALUES 
('Salario', 1, 1),
('Comida', 2, 2),
('Transporte', 2, 2),
('Café diario', 2, 3),
('Ahorro inversión', 1, 4);

-- CUENTA USUARIO
INSERT INTO CuentaUsuario (Contrasena, NombreUsuario, IdCliente)
VALUES 
('12345', 'juanp', 1),
('12345', 'mariag', 2),
('12345', 'luism', 3);

-- CORREO
INSERT INTO Correo (Correo, IdCliente)
VALUES 
('juan@gmail.com', 1),
('maria@gmail.com', 2),
('luis@gmail.com', 3);

-- TELEFONO
INSERT INTO Telefono (Telefono, IdCliente)
VALUES 
('5551-1111', 1),
('5552-2222', 2),
('5553-3333', 3);

-- MOVIMIENTO
INSERT INTO Movimiento (Concepto, Monto, FechaMovimiento, IdCliente, IdTipo, IdCategoria)
VALUES 
('Salario mensual', 5000, GETDATE(), 1, 1, 1),
('Compra supermercado', 800, GETDATE(), 1, 2, 2),
('Café', 25, GETDATE(), 1, 2, 4),
('Transporte bus', 15, GETDATE(), 2, 2, 3);

-- GASTO RECURRENTE
INSERT INTO GastoRecurrente (Concepto, Monto, FechaInicio, Frecuencia, IdCliente, Activo)
VALUES 
('Internet', 250, GETDATE(), 'Mensual', 1, 1),
('Netflix', 120, GETDATE(), 'Mensual', 2, 1);

-- METAS DE AHORRO
INSERT INTO MetasAhorro (IdUsuario, NombreMeta, MontoObjetivo, FechaLimite, MontoActual)
VALUES 
(1, 'Viaje a Japón', 15000, '2026-12-31', 2000),
(2, 'Comprar Laptop', 8000, '2026-08-15', 1500),
(3, 'Fondo de Emergencia', 10000, '2027-01-01', 3000);

-- PRESUPUESTO MENSUAL
INSERT INTO PresupuestoMensual (MontoPresupuesto, IdCategoria, MesAplicacion, IdUsuario)
VALUES 
(3000, 2, 'Enero', 1),
(2000, 3, 'Enero', 2);

-- ALERTA (PRUEBA)
INSERT INTO Alerta (IdUsuario, IdCategoria, TipoAlerta, Mensaje, Gastado, LimitePresupuesto, Porcentaje, Mes, Anio)
VALUES 
(1, 2, 'ALERTA', 'Has alcanzado el 80% del presupuesto', 2400, 3000, 80, 1, 2026);


------------------------------------------------------------
            --SP DE LA BASE DE DATOS
------------------------------------------------------------

-- 1. SP para Registrar un Ingreso (Fuerza el IdTipo = 1)
CREATE PROCEDURE sp_RegistrarIngreso
    @Concepto VARCHAR(30),
    @Monto DECIMAL(12,2),
    @IdCliente INT,
    @IdCategoria INT
AS
BEGIN
    DECLARE @NuevoId INT;
    
    INSERT INTO Movimiento (Concepto, Monto, FechaMovimiento, IdCliente, IdTipo,  IdCategoria)
    VALUES (@Concepto, @Monto, GETDATE(), @IdCliente, 1, @IdCategoria);
    
    SET @NuevoId = SCOPE_IDENTITY();
    
    SELECT IdMovimiento, Concepto, Monto, FechaMovimiento, IdCliente, IdTipo, IdCategoria
    FROM Movimiento 
    WHERE IdMovimiento = @NuevoId;
END;
GO

-- 2. SP para Editar un Ingreso (Asegurando que solo afecte a IdTipo = 1)
CREATE PROCEDURE sp_EditarIngreso
    @IdMovimiento INT,
    @Concepto VARCHAR(30),
    @Monto DECIMAL(12,2),
    @IdCategoria INT
AS
BEGIN
    UPDATE Movimiento
    SET Concepto = @Concepto,
        Monto = @Monto,
        IdCategoria = @IdCategoria
    WHERE IdMovimiento = @IdMovimiento AND IdTipo = 1;
    
    SELECT IdMovimiento, Concepto, Monto, FechaMovimiento, IdCliente, IdTipo, IdCategoria
    FROM Movimiento 
    WHERE IdMovimiento = @IdMovimiento;
END;
GO

--3. SP para Obtener Movimientos del Mes Actual (con JOIN para traer el nombre del tipo)
CREATE PROCEDURE sp_ObtenerMovimientosMesActual
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

--4. SP para Filtrar Movimientos por Mes y Año (con validaciones)
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
GO
-- 5. SP para Crear Meta de Ahorro (con validaciones)
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

-- 6. SP para Crear Presupuesto Mensual (con validaciones y manejo de errores)
CREATE OR ALTER PROCEDURE sp_CrearPresupuesto
(
    @MontoPresupuesto DECIMAL(12,2),
    @IdCategoria INT = NULL,
    @MesAplicacion VARCHAR(20),
    @IdUsuario INT,
    @PorcentajeAlerta INT = 80
)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY

        IF NOT EXISTS (SELECT 1 FROM Cliente WHERE IdCliente = @IdUsuario)
            THROW 50001, 'El usuario no existe', 1;

        IF @MontoPresupuesto <= 0
            THROW 50002, 'El monto debe ser mayor a 0', 1;

        -- Corrección de contingencia: Si es nulo, toma la primera categoría disponible si 'General' no existe
        IF @IdCategoria IS NULL
        BEGIN
            SELECT TOP 1 @IdCategoria = IdCategoria
            FROM CategoriaMovimiento
            WHERE NombreCategoria = 'General';
            
            IF @IdCategoria IS NULL
                SELECT TOP 1 @IdCategoria = IdCategoria FROM CategoriaMovimiento;
        END

        IF NOT EXISTS (SELECT 1 FROM CategoriaMovimiento WHERE IdCategoria = @IdCategoria)
            THROW 50003, 'La categoria no existe', 1;

        IF @MesAplicacion IS NULL OR LTRIM(RTRIM(@MesAplicacion)) = ''
            THROW 50004, 'Debe ingresar el mes de aplicacion', 1;

        IF EXISTS (
            SELECT 1
            FROM PresupuestoMensual
            WHERE IdUsuario = @IdUsuario
              AND IdCategoria = @IdCategoria
              AND MesAplicacion = @MesAplicacion
        )
            THROW 50005, 'Ya existe un presupuesto para esta categoria y mes', 1;

        INSERT INTO PresupuestoMensual (MontoPresupuesto, IdCategoria, MesAplicacion, IdUsuario, PorcentajeAlerta)
        VALUES (@MontoPresupuesto, @IdCategoria, @MesAplicacion, @IdUsuario, @PorcentajeAlerta);

        -- CORRECCIÓN CRÍTICA: Retornamos p.IdCategoria para que el API y el JS tengan el ID numérico
        SELECT
            p.IdPresupuesto,
            p.MontoPresupuesto,
            c.NombreCategoria AS Categoria,
            p.MesAplicacion,
            p.IdUsuario,
            p.IdCategoria, -- 👈 Enviado explícitamente al mapeo de Python
            p.PorcentajeAlerta
        FROM PresupuestoMensual p
        INNER JOIN CategoriaMovimiento c ON p.IdCategoria = c.IdCategoria
        WHERE p.IdPresupuesto = SCOPE_IDENTITY();

    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END;
GO
-- 7. SP para Validar Presupuesto Mensual (Calcula el porcentaje gastado y retorna estado)
CREATE OR ALTER PROCEDURE sp_ValidarPresupuesto
(
    @IdUsuario INT,
    @IdCategoria INT
)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @TotalGastado DECIMAL(12,2) = 0;
    DECLARE @MontoPresupuesto DECIMAL(12,2) = 0;
    DECLARE @PorcentajeUsado DECIMAL(12,2) = 0;
    DECLARE @PorcentajeAlerta DECIMAL(5,2) = 80;
    DECLARE @Estado VARCHAR(30) = 'NORMAL';
    DECLARE @NombreCategoria VARCHAR(50) = 'Sin Categoría';

    BEGIN TRY
        -- 1. Obtener los datos del presupuesto
        SELECT TOP 1
            @MontoPresupuesto = p.MontoPresupuesto,
            @PorcentajeAlerta = p.PorcentajeAlerta,
            @NombreCategoria = c.NombreCategoria
        FROM PresupuestoMensual p
        INNER JOIN CategoriaMovimiento c ON p.IdCategoria = c.IdCategoria
        WHERE p.IdUsuario = @IdUsuario
          AND p.IdCategoria = @IdCategoria;

        -- Si no hay presupuesto, enviamos valores vacíos limpios para que el JS no se rompa
        IF @MontoPresupuesto IS NULL OR @MontoPresupuesto = 0
        BEGIN
            SELECT 
                ISNULL(@NombreCategoria, 'Sin Presupuesto') AS categoria, 
                'NORMAL' AS estado, 
                0.00 AS gastado, 
                0.00 AS limite_presupuesto, 
                0.00 AS porcentaje_usado, 
                0 AS mostrar_alerta;
            RETURN;
        END

        -- 2. Calcular gasto real usando el MES y AÑO de los movimientos reales (IdTipo = 2 es Egreso)
        SELECT
            @TotalGastado = ISNULL(SUM(Monto), 0)
        FROM Movimiento
        WHERE IdCliente = @IdUsuario
          AND IdCategoria = @IdCategoria
          AND IdTipo = 2
          AND MONTH(FechaMovimiento) = MONTH(GETDATE())  -- 👈 Filtro dinámico real por mes numérico
          AND YEAR(FechaMovimiento) = YEAR(GETDATE());

        -- 3. Calcular porcentaje de forma segura
        SET @PorcentajeUsado = (@TotalGastado / @MontoPresupuesto) * 100;

        -- 4. Evaluar estados para los colores de la barra
        IF @PorcentajeUsado >= 100
            SET @Estado = 'EXCEDIDO';
        ELSE IF @PorcentajeUsado >= @PorcentajeAlerta
            SET @Estado = 'ALERTA';

        -- 5. RESPUESTA LIMPIA DIRECTA PARA TU API
        SELECT
            @NombreCategoria AS categoria,
            @Estado AS estado,
            @TotalGastado AS gastado,
            @MontoPresupuesto AS limite_presupuesto,
            ROUND(@PorcentajeUsado, 2) AS porcentaje_usado,
            CASE WHEN @Estado = 'NORMAL' THEN 0 ELSE 1 END AS mostrar_alerta;

    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END;
GO
-- 8. SP para Recalcular Presupuesto (Recalcula el porcentaje gastado y actualiza alertas)
CREATE OR ALTER PROCEDURE sp_RecalcularPresupuestoPorUsuario
(
    @IdUsuario INT
)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @IdCategoria INT;
    DECLARE @MontoPresupuesto DECIMAL(12,2);
    DECLARE @TotalGastado DECIMAL(12,2);
    DECLARE @Porcentaje DECIMAL(5,2);
    DECLARE @Umbral DECIMAL(5,2);
    DECLARE @Estado VARCHAR(20);

    -- recorrer presupuestos del usuario
    DECLARE cur CURSOR FOR
        SELECT IdCategoria, MontoPresupuesto, PorcentajeAlerta
        FROM PresupuestoMensual
        WHERE IdUsuario = @IdUsuario;

    OPEN cur;

    FETCH NEXT FROM cur INTO @IdCategoria, @MontoPresupuesto, @Umbral;

    WHILE @@FETCH_STATUS = 0
    BEGIN

        -- si no hay presupuesto no hacemos nada
        IF @MontoPresupuesto IS NULL OR @MontoPresupuesto = 0
        BEGIN
            FETCH NEXT FROM cur INTO @IdCategoria, @MontoPresupuesto, @Umbral;
            CONTINUE;
        END

        -- gasto del mes
        SELECT @TotalGastado = ISNULL(SUM(Monto),0)
        FROM Movimiento
        WHERE IdCliente = @IdUsuario
          AND IdCategoria = @IdCategoria
          AND IdTipo = 2
          AND MONTH(FechaMovimiento) = MONTH(GETDATE())
          AND YEAR(FechaMovimiento) = YEAR(GETDATE());

        SET @Porcentaje = (@TotalGastado / @MontoPresupuesto) * 100;

        -- estado
        IF @Porcentaje >= 100
            SET @Estado = 'EXCEDIDO';
        ELSE IF @Porcentaje >= @Umbral
            SET @Estado = 'ALERTA';
        ELSE
            SET @Estado = 'NORMAL';

        -- evitar duplicados y actualizar alerta lógica
        IF @Estado <> 'NORMAL'
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM Alerta
                WHERE IdUsuario = @IdUsuario
                  AND IdCategoria = @IdCategoria
                  AND Mes = MONTH(GETDATE())
                  AND Anio = YEAR(GETDATE())
                  AND TipoAlerta = @Estado
            )
            BEGIN
                INSERT INTO Alerta(
                    IdUsuario, IdCategoria, TipoAlerta,
                    Mensaje, Gastado, LimitePresupuesto,
                    Porcentaje, Mes, Anio
                )
                VALUES (
                    @IdUsuario,
                    @IdCategoria,
                    @Estado,
                    'Alerta automática por presupuesto',
                    @TotalGastado,
                    @MontoPresupuesto,
                    @Porcentaje,
                    MONTH(GETDATE()),
                    YEAR(GETDATE())
                );
            END
        END

        FETCH NEXT FROM cur INTO @IdCategoria, @MontoPresupuesto, @Umbral;
    END

    CLOSE cur;
    DEALLOCATE cur;

END;
GO
-- 9. SP para Obtener Resumen de Presupuestos (Trae el porcentaje gastado y estado para cada presupuesto)
CREATE OR ALTER PROCEDURE sp_ObtenerResumenPresupuestos
(
    @IdUsuario INT
)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        c.NombreCategoria AS categoria,
        p.MontoPresupuesto AS limite,
        ISNULL(SUM(m.Monto),0) AS gastado,
        CASE 
            WHEN p.MontoPresupuesto = 0 THEN 0
            ELSE ROUND((ISNULL(SUM(m.Monto),0) / p.MontoPresupuesto) * 100, 2)
        END AS porcentaje,
        CASE 
            WHEN p.MontoPresupuesto = 0 THEN 'SIN_DATOS'
            WHEN (ISNULL(SUM(m.Monto),0) / p.MontoPresupuesto) * 100 >= 100 THEN 'EXCEDIDO'
            WHEN (ISNULL(SUM(m.Monto),0) / p.MontoPresupuesto) * 100 >= p.PorcentajeAlerta THEN 'ALERTA'
            ELSE 'NORMAL'
        END AS estado
    FROM PresupuestoMensual p
    INNER JOIN CategoriaMovimiento c
        ON p.IdCategoria = c.IdCategoria
    LEFT JOIN Movimiento m
        ON m.IdCategoria = p.IdCategoria
        AND m.IdCliente = p.IdUsuario
        AND m.IdTipo = 2
        AND MONTH(m.FechaMovimiento) = MONTH(GETDATE())
        AND YEAR(m.FechaMovimiento) = YEAR(GETDATE())
    WHERE p.IdUsuario = @IdUsuario
    GROUP BY 
        c.NombreCategoria,
        p.MontoPresupuesto,
        p.PorcentajeAlerta;
END;
GO