ALTER TABLE matriculadisciplinas RENAME TO inscricoes;

ALTER TABLE disciplinas ADD CONSTRAINT id_disciplina_pk PRIMARY KEY (id_disciplina);
ALTER TABLE docentes ADD CONSTRAINT id_docente_pk PRIMARY KEY (id_docente);
ALTER TABLE discentes ADD CONSTRAINT id_discente_pk PRIMARY KEY (id_discente);
ALTER TABLE inscricoes ADD CONSTRAINT id_matriculadisciplina_pk PRIMARY KEY (id_matriculadisciplina);

ALTER TABLE docentes ADD CONSTRAINT id_disciplina__docentes_to_disciplinas_fk FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id_disciplina);
ALTER TABLE inscricoes ADD CONSTRAINT id_docente__inscricoes_to_docentes_fk FOREIGN KEY (id_docente) REFERENCES docentes(id_docente);
ALTER TABLE inscricoes ADD CONSTRAINT id_discente__inscricoes_to_discentes_fk FOREIGN KEY (id_discente) REFERENCES discentes(id_discente);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO consumer;
-- REVOKE ALL PRIVILEGES ON TABLE discente FROM consumer;