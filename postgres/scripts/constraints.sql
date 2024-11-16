

ALTER TABLE disciplinas ADD CONSTRAINT id_disciplina_pk PRIMARY KEY (id_disciplina);
ALTER TABLE docentes ADD CONSTRAINT id_docente_pk PRIMARY KEY (matricula);
ALTER TABLE discentes ADD CONSTRAINT id_discente_pk PRIMARY KEY (matricula);
ALTER TABLE matriculadisciplinas ADD CONSTRAINT id_matriculadisciplina_pk PRIMARY KEY (id_matricula);


ALTER TABLE disciplinas ADD CONSTRAINT matricula_docente__disciplinas_to_docentes_fk FOREIGN KEY (matricula_docente) REFERENCES docentes(matricula);
ALTER TABLE matriculadisciplinas ADD CONSTRAINT id_disciplina__matriculadisciplinas_to_disciplinas_fk FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id_disciplina);
ALTER TABLE matriculadisciplinas ADD CONSTRAINT matricula_docente__matriculadisciplinas_to_docentes_fk FOREIGN KEY (matricula_docente) REFERENCES docentes(matricula);
ALTER TABLE matriculadisciplinas ADD CONSTRAINT matricula_discente__matriculadisciplinas_to_discentes_fk FOREIGN KEY (matricula_discente) REFERENCES discentes(matricula);


ALTER TABLE discentes ENABLE ROW LEVEL SECURITY;
ALTER TABLE docentes ENABLE ROW LEVEL SECURITY;
ALTER TABLE disciplinas ENABLE ROW LEVEL SECURITY;
ALTER TABLE matriculadisciplinas ENABLE ROW LEVEL SECURITY;


-- Policy for SELECT operations
CREATE POLICY select_docentes ON docentes
    FOR SELECT USING(true);
CREATE POLICY select_disciplinas ON disciplinas
    FOR SELECT USING(true);

CREATE POLICY consumer_select_discentes ON discentes
    FOR SELECT USING(current_user = 'consumer');
CREATE POLICY consumer_select_matriculadisciplinas ON matriculadisciplinas
    FOR SELECT USING(current_user = 'consumer');

CREATE POLICY professor_select_discentes ON discentes
    FOR SELECT
    USING (
        current_user = 'professor'
        AND curso IN (SELECT curso FROM docentes WHERE matricula = 2)
    );
CREATE POLICY professor_select_matriculas ON matriculadisciplinas
    FOR SELECT
    USING (
        current_user = 'professor'
        AND matricula_docente = 2
    );


-- Policy for UPDATE operations
CREATE POLICY consumer_modification_disciplinas ON disciplinas
    FOR UPDATE USING (current_user = 'consumer');
CREATE POLICY consumer_modification_matriculas ON matriculadisciplinas
    FOR UPDATE USING (current_user = 'consumer');
CREATE POLICY consumer_modification_discentes ON discentes
    FOR UPDATE USING (current_user = 'consumer');
CREATE POLICY consumer_modification_docentes ON docentes
    FOR UPDATE USING (current_user = 'consumer');

CREATE POLICY professor_modification_docentes ON docentes 
    FOR UPDATE
    USING (current_user = 'professor')
    WITH CHECK (
        current_user = 'professor'
        AND matricula = 2
    );
CREATE POLICY professor_modification_matriculas ON matriculadisciplinas 
    FOR UPDATE
    USING (current_user = 'professor')
    WITH CHECK (
        current_user = 'professor'
        AND matricula_docente = 2
    );
CREATE POLICY professor_modification_disciplinas ON disciplinas 
    FOR UPDATE
    USING (current_user = 'professor')
    WITH CHECK (
        current_user = 'professor'
        AND matricula_docente = 2
    );


GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO consumer;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO professor;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA relatorios TO consumer;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA relatorios TO professor;
-- REVOKE ALL PRIVILEGES ON TABLE discente FROM consumer;
