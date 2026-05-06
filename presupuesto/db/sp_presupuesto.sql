-- SP para registrar presupuesto con validación
-- Valida user_id en users, category en categories o 'General'
-- INSERT OR REPLACE en budgets

CREATE OR REPLACE PROCEDURE sp_registrar_presupuesto(
    IN p_user_id INTEGER,
    IN p_month TEXT,
    IN p_category TEXT,
    IN p_amount REAL
) AS $$
BEGIN
    -- Validate user
    IF NOT EXISTS (SELECT 1 FROM users WHERE id = p_user_id) THEN
        SELECT 0 as success;  -- Fail
        RETURN;
    END IF;
    
    -- Category: exists or 'General'
    DECLARE v_category TEXT := COALESCE(p_category, 'General');
    IF p_category IS NOT NULL AND NOT EXISTS (SELECT 1 FROM categories WHERE name = p_category) THEN
        SELECT 0 as success;
        RETURN;
    END IF;
    
    -- Insert/Replace
    INSERT OR REPLACE INTO budgets (user_id, month, category, amount)
    VALUES (p_user_id, p_month, v_category, p_amount);
    
    SELECT 1 as success;
END;
$$;
