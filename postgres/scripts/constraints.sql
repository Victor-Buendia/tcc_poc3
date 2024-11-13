-- ALTER TABLE matriculadisciplinas RENAME TO inscricoes;

ALTER TABLE disciplinas ADD CONSTRAINT id_disciplina_pk PRIMARY KEY (id_disciplina);
ALTER TABLE docentes ADD CONSTRAINT id_docente_pk PRIMARY KEY (matricula);
ALTER TABLE discentes ADD CONSTRAINT id_discente_pk PRIMARY KEY (matricula);
ALTER TABLE matriculadisciplinas ADD CONSTRAINT id_matriculadisciplina_pk PRIMARY KEY (id_matricula);

ALTER TABLE disciplinas ADD CONSTRAINT matricula_docente__disciplinas_to_docentes_fk FOREIGN KEY (matricula_docente) REFERENCES docentes(matricula);
ALTER TABLE matriculadisciplinas ADD CONSTRAINT id_disciplina__matriculadisciplinas_to_disciplinas_fk FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id_disciplina);
ALTER TABLE matriculadisciplinas ADD CONSTRAINT matricula_docente__matriculadisciplinas_to_docentes_fk FOREIGN KEY (matricula_docente) REFERENCES docentes(matricula);
ALTER TABLE matriculadisciplinas ADD CONSTRAINT matricula_discente__matriculadisciplinas_to_discentes_fk FOREIGN KEY (matricula_discente) REFERENCES discentes(matricula);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO consumer;
-- REVOKE ALL PRIVILEGES ON TABLE discente FROM consumer;