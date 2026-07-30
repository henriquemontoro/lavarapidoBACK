from functools import lru_cache

# Cópia integral do POP (Procedimento Operacional Padrão da Jornada do
# Veículo — Serviços e Planos de Assinatura, Lava-Rápido Nogueira), versão
# 3.2. Fonte de conhecimento do assistente: mantém aqui em vez de ler de um
# caminho externo pra ficar versionado junto do código.
_POP_DOCUMENTO = """\
# POP: Procedimento Operacional Padrão da Jornada do Veículo — Serviços e Planos de Assinatura (Lava-Rápido Nogueira)

## Metadados
- Nome do Processo: Procedimento Operacional Padrão da Jornada do Veículo — Serviços e Planos de Assinatura (Lava-Rápido Nogueira)
- Código do Documento: POP-OPE-001
- Versão: 3.2
- Elaborador: Equipe de consultoria — Insper Jr, 51ª Gestão (Case I – Capacitação 2026.2)
- Aprovador: Proprietário
- Data de Elaboração: 29/07/2026
- Data de Vigência / Próxima Revisão: 31/07/2026

## Objetivo
Padronizar a jornada completa do veículo no Lava-Rápido Nogueira, do momento em que o veículo cruza o portão até a entrega da chave ao cliente, abrangendo todos os serviços do catálogo e o atendimento a Cliente Assinante, de modo que o resultado entregue não dependa de qual colaborador executou o serviço nem da presença do Proprietário no pátio. O procedimento existe para eliminar cinco perdas: veículo que entra e não é atendido; veículo que perde o registro e para no fluxo; retrabalho detectado somente pelo cliente; veículo pronto que permanece parado sem que o cliente seja avisado; e serviço de Cliente Assinante executado sem débito do saldo ou cobrado indevidamente. Toda informação que hoje está retida apenas na memória do Proprietário passa a estar registrada no Dashboard.

## Escopo
- Aplica-se a: Aplica-se a todos os colaboradores do Lava-Rápido Nogueira, em todos os dias de funcionamento, de segunda a segunda, das 08:00 às 17:00. Aplica-se a todos os serviços do catálogo: Lavagem Simples, Lavagem Completa, Lavagem de Motor, Polimento, Cera, Higienização de Bancos e Lavagem Detalhada. Aplica-se a todas as categorias de cliente: Cliente Assinante, Cliente de Conta Faturada, Cliente Recorrente Cadastrado e Cliente Eventual. Aplica-se também à venda e à adesão de Plano de Assinatura, realizadas pelo Atendente. A operação do pátio é comandada pelo Gerente, a quem os Colaboradores estão subordinados. Não há distinção de função entre os Colaboradores: qualquer Colaborador está habilitado a executar qualquer serviço do catálogo e a manobrar veículos dentro da unidade.
- Não se aplica a: Não se aplica à lavagem de chassi. Não cobre o agendamento prévio de horário, que não existe na operação. Não cobre a configuração, a alimentação nem a manutenção do Dashboard e da plataforma Portal Nogueira. Não cobre a rotina de fechamento de caixa nem a emissão de nota fiscal. Não cobre a rotina de recrutamento, integração e treinamento de novos colaboradores, que demanda POP próprio. Não cobre a cobrança recorrente dos Planos de Assinatura, limitando-se a definir o tratamento operacional do Plano Inativo.

## Materiais e Sistemas
Estrutura física: 3 Boxes de Lavagem operacionais; Container de Polimento; Ponto de Aspiração fixo; Ponto de Lavagem de Tapetes; Vaga de Recepção demarcada; Vaga de Entrega, com capacidade de 2 a 3 veículos; Vagas do Fundo, destinadas a veículos em secagem ou aguardando retirada, acessadas por Corredor de Acesso único de 3,5 m de largura; portão único com vão de 4,5 m. Equipamentos: 3 máquinas de alta pressão em condição de uso; aspirador; compressor de ar; escova e bomba de lavagem de tapetes; politriz. Insumos: shampoo automotivo; luva de lavagem; toalha de carroceria; toalha exclusiva para vidros; pano de painel; cera; massa de polimento; produto de higienização para couro e para tecido; desengraxante de motor; pretinho de pneu; aromatizante. Registros e controles: Dashboard, sistema único de registro da operação; tablets de acesso ao Dashboard no pátio; plataforma Portal Nogueira, onde são assinados o Termo de Adesão e o Termo de Prestação de Serviço; Quadro de Chaves com ganchos numerados; Checklist de Conferência Final; Ficha de Preferências do Cliente; Registro de Retrabalho; Registro de Demanda Não Atendida; Registro de Anomalias; WhatsApp corporativo com chatbot. O Dashboard é acessado no pátio por tablet, de modo que o Colaborador consulta a Ordem de Serviço no próprio Box de Lavagem e registra ali a conclusão de cada serviço. Tabela de Tempos-Padrão, integrante deste procedimento e utilizada no cálculo do Tempo Prometido de Entrega.

## Glossário
- **Dashboard**: Sistema único de registro da operação, no qual são abertas as Ordens de Serviço, registrada a Vistoria de Entrada, consultado e debitado o Saldo de Serviços dos Planos de Assinatura, e registrada a conclusão de cada etapa. Substitui integralmente a comanda em papel, que deixa de existir. É a única fonte válida de consulta e de registro.
- **Portal Nogueira**: Plataforma na qual o cliente assina o Termo de Adesão vinculado ao Termo de Prestação de Serviço para contratar Plano de Assinatura.
- **Ordem de Serviço**: Registro digital aberto no Dashboard no momento da recepção do veículo, contendo: número, placa, modelo, cor, nome e telefone do cliente, serviços contratados, Modalidade de Atendimento, hora de entrada, Tempo Prometido de Entrega, resultado da Vistoria de Entrada, conclusão de cada etapa, valor cobrado, forma de pagamento e hora de saída. Termo canônico que substitui os usos informais 'comanda', 'papel' e 'bloco'.
- **Modalidade de Atendimento**: Campo obrigatório da Ordem de Serviço que classifica cada serviço contratado em uma de quatro condições: Assinatura, quando debitado do Saldo de Serviços; Excedente, quando o saldo do serviço está esgotado; Conta Faturada; ou Avulso. Uma mesma Ordem de Serviço pode conter serviços em modalidades distintas.
- **Lavagem Simples**: Serviço de lavagem exclusivamente externa do veículo, executado conforme as etapas 27 a 34 deste procedimento. Preço de 50 reais, igual para qualquer porte de veículo.
- **Lavagem Completa**: Serviço de lavagem externa e interna do veículo, executado conforme as etapas 27 a 43 deste procedimento. Preço de 90 reais, igual para qualquer porte de veículo. Termo canônico que substitui os usos informais 'completa' e a marcação 'C'.
- **Lavagem de Motor**: Serviço de limpeza do compartimento do motor. Preço de 35 reais, igual para qualquer porte de veículo. É sempre o primeiro serviço executado no veículo, antes de qualquer lavagem, porque a água e a sujeira do compartimento escorrem sobre a carroceria.
- **Polimento**: Serviço de correção da pintura executado no Container de Polimento, com uso de politriz. Preço de 500 reais, igual para qualquer porte de veículo. Tempo-padrão de 240 minutos. É sempre executado depois da lavagem e antes da Cera.
- **Cera**: Serviço de aplicação de camada de proteção sobre a pintura. Preço de 30 reais, igual para qualquer porte de veículo. Só pode ser executado sobre veículo limpo, e é sempre executado depois da lavagem e depois do Polimento, quando este for contratado.
- **Higienização de Bancos**: Serviço de higienização dos bancos do veículo, cobrado pelo veículo inteiro e não por banco. Preço de 75 reais para bancos de couro e de 50 reais para bancos de tecido, igual para qualquer porte de veículo. É sempre o último serviço executado. Tempo-padrão de 120 minutos para couro e de 100 minutos para tecido, já incluída a secagem.
- **Lavagem Detalhada**: Serviço de escopo variável, sem preço de tabela. O orçamento é elaborado pelo colaborador mais experiente presente na unidade no momento da solicitação.
- **Catálogo de Serviços**: Conjunto dos serviços oferecidos pela unidade, com preços fixos e iguais para qualquer porte de veículo: Lavagem Simples, 50 reais; Lavagem Completa, 90 reais; Cera, 30 reais; Polimento, 500 reais; Lavagem de Motor, 35 reais; Higienização de Bancos de couro, 75 reais; Higienização de Bancos de tecido, 50 reais; e Lavagem Detalhada, sob orçamento.
- **Tabela de Tempos-Padrão**: Conjunto dos tempos médios de execução de cada serviço, utilizado para calcular o Tempo Prometido de Entrega: Lavagem Simples, 20 minutos; Lavagem Completa, 60 minutos; Lavagem de Motor, 60 minutos; Polimento, 240 minutos; Cera, 20 minutos; Higienização de Bancos de couro, 120 minutos; Higienização de Bancos de tecido, 100 minutos. Os tempos de Higienização de Bancos já contemplam a secagem. A Lavagem Detalhada não possui tempo-padrão e tem o prazo definido no orçamento. Os tempos são médios e revisáveis: alteram-se ao longo do tempo conforme as cronometragens e os cálculos realizados pelo Gerente. Por integrarem o corpo deste procedimento, qualquer alteração na Tabela de Tempos-Padrão constitui revisão formal do documento, sujeita à aprovação do Proprietário e a registro no Histórico de Revisões.
- **Ordem de Execução dos Serviços**: Sequência obrigatória de execução quando mais de um serviço é contratado para o mesmo veículo: Lavagem de Motor, depois Lavagem Simples ou Lavagem Completa, depois Polimento, depois Cera, e por último Higienização de Bancos. É proibido alterar essa sequência.
- **Plano de Assinatura**: Contrato de pagamento mensal recorrente que dá ao cliente direito a uma quantidade determinada de serviços por Ciclo de Assinatura. A unidade oferece três planos: Bronze, por 129,99 reais, com 2 Lavagens Completas e 1 Cera; Prata, por 229,99 reais, com 4 Lavagens Completas e 2 Ceras; e Ouro, por 259,99 reais, com 6 Lavagens Completas e 3 Ceras.
- **Ciclo de Assinatura**: Período de 30 dias corridos contados da data de adesão do cliente ao Plano de Assinatura, ao fim do qual o Saldo de Serviços é renovado. Cada Cliente Assinante possui ciclo próprio, que não coincide com o mês-calendário nem com o ciclo dos demais assinantes.
- **Saldo de Serviços**: Quantidade de serviços ainda não utilizados dentro do Ciclo de Assinatura em curso. O Plano de Assinatura possui dois contadores independentes, um de Lavagens Completas e outro de Ceras, que não se convertem um no outro. Saldo não utilizado de qualquer um dos dois expira ao fim do ciclo e não é acumulado para o ciclo seguinte.
- **Serviço Excedente**: Serviço solicitado por Cliente Assinante cujo Saldo de Serviços correspondente está esgotado. É cobrado pelo preço cheio do Catálogo de Serviços, sem desconto de assinante.
- **Plano Inativo**: Situação do Plano de Assinatura cuja cobrança recorrente não foi liquidada. A passagem à condição de Plano Inativo é imediata, sem prazo de tolerância. O Cliente Assinante com Plano Inativo não dispõe de Saldo de Serviços e é atendido mediante pagamento do preço cheio do Catálogo de Serviços.
- **Termo de Adesão**: Documento assinado pelo cliente na plataforma Portal Nogueira, vinculado ao Termo de Prestação de Serviço, que formaliza a contratação do Plano de Assinatura e estabelece a data de início do primeiro Ciclo de Assinatura.
- **Box de Lavagem**: Posto coberto onde se executam a Lavagem de Motor, a Lavagem Simples e a Lavagem Completa. A unidade possui três, identificados como Box 1, Box 2 e Box 3, todos operacionais em todos os dias de funcionamento.
- **Container de Polimento**: Espaço destinado exclusivamente à execução do Polimento. Por ser espaço próprio, o Polimento não ocupa Box de Lavagem e não reduz a capacidade de lavagem da unidade.
- **Ponto de Aspiração**: Posição fixa, situada junto ao muro lateral, onde se executa a aspiração do veículo. Por ser fixa, exige o deslocamento do veículo do Box de Lavagem até ela.
- **Ponto de Lavagem de Tapetes**: Posição onde ficam instaladas a escova e a bomba destinadas à lavagem dos tapetes retirados do veículo.
- **Vaga de Recepção**: Vaga demarcada, situada imediatamente após o portão, destinada exclusivamente ao veículo que acaba de entrar e ainda não teve Ordem de Serviço aberta. Não pode ser utilizada para estacionar veículo pronto nem veículo em espera.
- **Vaga de Entrega**: Área situada na frente da unidade, próxima ao portão, com capacidade de 2 a 3 veículos, destinada exclusivamente a veículos aprovados na Conferência Final que aguardam retirada imediata pelo cliente.
- **Vagas do Fundo**: Vagas situadas nos fundos do terreno, destinadas a veículos em secagem após Higienização de Bancos e a veículos prontos cuja retirada não é imediata. Ligadas à área frontal pelo Corredor de Acesso, operam em regime de último a entrar, primeiro a sair: para retirar um veículo posicionado ao fundo é necessário remover antes todos os veículos posicionados à sua frente.
- **Corredor de Acesso**: Passagem única, de 3,5 m de largura, que liga a área frontal da unidade às Vagas do Fundo. Não permite tráfego simultâneo em dois sentidos.
- **Vistoria de Entrada**: Conferência do estado do veículo realizada na presença do cliente, antes do recebimento da chave, registrando no Dashboard avarias visíveis, nível de sujeira e objetos aparentes no interior. Não existia na operação anterior a este procedimento.
- **Tempo Prometido de Entrega**: Horário de conclusão informado ao cliente no momento da abertura da Ordem de Serviço, obtido pela soma dos tempos-padrão de todos os serviços contratados, conforme a Tabela de Tempos-Padrão, acrescida do tempo de espera decorrente dos veículos já em fila. Não é estimativa pessoal do Atendente.
- **Conferência Final**: Inspeção obrigatória de todo veículo, aplicando o Checklist de Conferência Final, executada pelo colaborador que concluiu o último serviço naquele veículo, antes de o veículo ser liberado para entrega.
- **Checklist de Conferência Final**: Lista fixa de itens verificados na Conferência Final, aplicada de forma idêntica a todos os veículos, com itens adicionais conforme os serviços contratados, de modo que o resultado não dependa de quem inspeciona.
- **Retrabalho**: Reexecução total ou parcial de uma etapa já concluída, motivada por reprovação na Conferência Final ou por apontamento do cliente no momento da entrega. Todo retrabalho é registrado no Registro de Retrabalho.
- **Registro de Retrabalho**: Registro que consolida data, placa, item reprovado, serviço de origem e colaborador responsável de cada Retrabalho, com a finalidade de identificar defeitos recorrentes.
- **Registro de Demanda Não Atendida**: Registro de todo cliente que procura a unidade e não é atendido, com data, hora, placa quando disponível, categoria do cliente e motivo da recusa. Existe porque a operação anterior recusava clientes em dias de pico sem qualquer registro do volume recusado.
- **Registro de Anomalias**: Registro de toda ocorrência prevista na seção Anomalias deste documento, contendo data, placa, descrição, ação adotada e desfecho.
- **Ficha de Preferências do Cliente**: Registro, por cliente, das exigências específicas já conhecidas da operação, como pontos de atenção na limpeza e dosagem de aromatizante. Existe para transferir para o Dashboard a informação que hoje está retida na memória do Proprietário e se perde quando ele não está presente.
- **Quadro de Chaves**: Quadro instalado no escritório, com ganchos numerados, destinado à guarda de toda chave de veículo sob responsabilidade da unidade. Cada gancho corresponde ao número da Ordem de Serviço do respectivo veículo, e é esse número que vincula o veículo físico ao seu registro no Dashboard.
- **Cliente Assinante**: Cliente titular de Plano de Assinatura vinculado a uma placa fixa. O plano não pode ser utilizado em veículo de placa distinta da cadastrada. Não possui prioridade sobre a ordem de chegada.
- **Cliente de Conta Faturada**: Pessoa jurídica ou pessoa física com acerto periódico de pagamento, cujo serviço não é cobrado no ato da entrega e não decorre de Plano de Assinatura.
- **Cliente Recorrente Cadastrado**: Cliente sem Plano de Assinatura, com Ficha de Preferências do Cliente preenchida e telefone registrado, que utiliza o serviço com regularidade e paga no ato da entrega.
- **Cliente Eventual**: Cliente sem Plano de Assinatura, sem Ficha de Preferências do Cliente e sem histórico registrado na unidade, incluindo o cliente de primeira visita.
- **Proprietário**: Papel responsável pela aprovação de exceções a este procedimento e por toda decisão de isenção, desconto ou reparo por conta da unidade, sem alçada delegada a outro papel.
- **Gerente**: Papel responsável pelo comando da operação no pátio, com autoridade hierárquica sobre os Colaboradores. Acompanha a execução dos serviços, verifica a conformidade com este procedimento, cronometra os tempos de execução, responde pela qualidade entregue e redistribui tarefas. É o papel que decide sobre a operação do dia; as decisões de isenção, desconto, reparo por conta da unidade e apuração de relato de desaparecimento de objeto permanecem exclusivas do Proprietário.
- **Atendente**: Papel responsável pelo primeiro contato com o cliente, pela consulta ao Dashboard, pela Vistoria de Entrada, pela abertura da Ordem de Serviço, pela definição do Tempo Prometido de Entrega, pela guarda da chave, pela venda de Plano de Assinatura, pela comunicação com o cliente e pela entrega do veículo.
- **Colaborador**: Papel responsável pela execução dos serviços do Catálogo de Serviços e pelo deslocamento de veículos dentro da unidade, entre Vaga de Recepção, Box de Lavagem, Container de Polimento, Ponto de Aspiração, Vagas do Fundo e Vaga de Entrega. Qualquer Colaborador está habilitado a executar qualquer serviço, inclusive Polimento e Higienização de Bancos. Termo canônico único, que substitui as denominações informais de função por posto, como lavador, manobrista e ajudante.
- **Responsável Administrativo**: Papel responsável pelo débito do Saldo de Serviços no Dashboard, pelo controle das contas de Cliente de Conta Faturada, pela manutenção da Ficha de Preferências do Cliente e pela consolidação dos registros.

## Matriz de Responsáveis (RACI)
- Tarefa "Manter a Vaga de Recepção desobstruída e sinalizada": o papel **Atendente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Realizar o primeiro contato com o cliente que entra na unidade": o papel **Atendente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Consultar a placa no Dashboard e verificar o Saldo de Serviços": o papel **Atendente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Registrar os serviços contratados e informar os preços do Catálogo de Serviços": o papel **Atendente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Elaborar o orçamento de Lavagem Detalhada": o papel **Colaborador** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Elaborar o orçamento de Lavagem Detalhada": o papel **Proprietário** tem responsabilidade *Informado*.
- Tarefa "Definir e informar o Tempo Prometido de Entrega": o papel **Atendente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Realizar a Vistoria de Entrada com o cliente presente": o papel **Atendente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Realizar a Vistoria de Entrada com o cliente presente": o papel **Cliente** tem responsabilidade *Consultado*.
- Tarefa "Abrir a Ordem de Serviço no Dashboard com todos os campos obrigatórios": o papel **Atendente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Receber a chave do cliente e guardá-la no gancho numerado do Quadro de Chaves": o papel **Atendente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Definir a posição do veículo na fila pela ordem de chegada": o papel **Atendente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Autorizar exceção à ordem de chegada da fila": o papel **Proprietário** tem responsabilidade *Aprovador*.
- Tarefa "Registrar cliente recusado no Registro de Demanda Não Atendida": o papel **Atendente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Deslocar veículos entre as posições internas da unidade": o papel **Colaborador** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Consultar a Ordem de Serviço no Dashboard antes de iniciar a execução": o papel **Colaborador** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Executar os serviços na Ordem de Execução dos Serviços": o papel **Colaborador** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Registrar no Dashboard a conclusão de cada serviço": o papel **Colaborador** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Aplicar aromatizante conforme a Ficha de Preferências do Cliente": o papel **Colaborador** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Executar a Conferência Final aplicando o Checklist de Conferência Final": o papel **Colaborador** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Registrar a ocorrência no Registro de Retrabalho": o papel **Colaborador** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Comunicar ao cliente a conclusão do serviço": o papel **Atendente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Comunicar ativamente ao cliente o atraso em relação ao Tempo Prometido de Entrega": o papel **Atendente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Comunicar ativamente ao cliente o atraso em relação ao Tempo Prometido de Entrega": o papel **Proprietário** tem responsabilidade *Informado*.
- Tarefa "Realizar a entrega do veículo com o cliente presente": o papel **Atendente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Receber o pagamento e registrar a forma de pagamento na Ordem de Serviço": o papel **Atendente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Vender Plano de Assinatura presencialmente ou pelo WhatsApp corporativo": o papel **Atendente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Conduzir a adesão do cliente ao Plano de Assinatura no Portal Nogueira": o papel **Atendente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Debitar o serviço do Saldo de Serviços no Dashboard": o papel **Responsável Administrativo** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Autorizar isenção, desconto ou reparo por conta da unidade": o papel **Proprietário** tem responsabilidade *Aprovador*.
- Tarefa "Conduzir a apuração de relato de desaparecimento de objeto": o papel **Proprietário** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Manter e atualizar a Ficha de Preferências do Cliente": o papel **Responsável Administrativo** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Controlar as contas de Cliente de Conta Faturada": o papel **Responsável Administrativo** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Consolidar mensalmente o Registro de Retrabalho, o Registro de Demanda Não Atendida e o Registro de Anomalias": o papel **Responsável Administrativo** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Consolidar mensalmente o Registro de Retrabalho, o Registro de Demanda Não Atendida e o Registro de Anomalias": o papel **Proprietário** tem responsabilidade *Informado*.
- Tarefa "Aprovar alterações neste procedimento": o papel **Proprietário** tem responsabilidade *Aprovador*.
- Tarefa "Comandar a operação do pátio e redistribuir tarefas entre os Colaboradores": o papel **Gerente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Cronometrar os tempos de execução dos serviços e registrar os tempos aferidos": o papel **Gerente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Verificar por amostragem a qualidade dos veículos aprovados na Conferência Final": o papel **Gerente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Determinar Retrabalho em veículo já aprovado na Conferência Final": o papel **Gerente** tem responsabilidade *Aprovador*.
- Tarefa "Corrigir desvio de procedimento identificado na execução": o papel **Gerente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Elaborar o orçamento de Lavagem Detalhada": o papel **Gerente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Apresentar ao Proprietário a consolidação dos tempos aferidos e dos desvios recorrentes": o papel **Gerente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Apresentar ao Proprietário a consolidação dos tempos aferidos e dos desvios recorrentes": o papel **Proprietário** tem responsabilidade *Informado*.
- Tarefa "Propor a recalibração da Tabela de Tempos-Padrão com base nos tempos aferidos": o papel **Gerente** tem responsabilidade *Responsável e Aprovador*.
- Tarefa "Aprovar a recalibração da Tabela de Tempos-Padrão e a revisão do procedimento": o papel **Proprietário** tem responsabilidade *Aprovador*.

## Procedimento
### Etapa 1 — Responsável: Atendente
Manter a Vaga de Recepção livre e sinalizada durante todo o horário de funcionamento, das 08:00 às 17:00, de segunda a segunda, sem exceção de dia da semana. SE a Vaga de Recepção estiver ocupada por veículo já pronto ENTÃO acionar o Colaborador para transferi-lo à Vaga de Entrega ou às Vagas do Fundo antes de receber novo veículo.

### Etapa 2 — Responsável: Atendente
Ao identificar veículo cruzando o portão, deslocar-se imediatamente até a Vaga de Recepção e estabelecer contato verbal com o cliente. É proibido deixar veículo estacionado na unidade sem contato verbal.

### Etapa 3 — Responsável: Atendente
SE todos os colaboradores estiverem com serviço em andamento no momento da entrada do veículo ENTÃO o colaborador que estiver na etapa de secagem ou de finalização interrompe sua tarefa e assume a recepção.

### Etapa 4 — Responsável: Atendente
Orientar verbalmente o cliente sobre a posição exata em que deve estacionar. É proibido permitir que o veículo permaneça obstruindo o portão ou o acesso interno.

### Etapa 5 — Responsável: Atendente
Registrar os serviços solicitados pelo cliente e consultar a placa do veículo no Dashboard antes de informar qualquer valor. O Dashboard é a única fonte válida de consulta; é proibido definir a condição de cobrança pela declaração verbal do cliente ou pela memória do colaborador.

### Etapa 6 — Responsável: Atendente
SE a placa não constar vinculada a Plano de Assinatura ENTÃO classificar todos os serviços com Modalidade de Atendimento Avulso, ou Conta Faturada quando o cliente possuir acerto periódico, e informar os preços do Catálogo de Serviços: Lavagem Simples 50 reais; Lavagem Completa 90 reais; Cera 30 reais; Polimento 500 reais; Lavagem de Motor 35 reais; Higienização de Bancos de couro 75 reais; Higienização de Bancos de tecido 50 reais. Os preços são iguais para qualquer porte de veículo.

### Etapa 7 — Responsável: Atendente
SE a placa constar vinculada a Plano de Assinatura ativo ENTÃO verificar separadamente os dois contadores do Saldo de Serviços, o de Lavagens Completas e o de Ceras. É proibido converter saldo de um contador no outro.

### Etapa 8 — Responsável: Atendente
SE o serviço solicitado for Lavagem Completa e o contador de Lavagens Completas for maior que zero ENTÃO classificar o serviço com Modalidade de Atendimento Assinatura, informar que não haverá cobrança no ato e informar o saldo restante após este atendimento.

### Etapa 9 — Responsável: Atendente
SE o serviço solicitado for Cera e o contador de Ceras for maior que zero ENTÃO classificar o serviço com Modalidade de Atendimento Assinatura, informar que não haverá cobrança no ato e informar o saldo restante após este atendimento.

### Etapa 10 — Responsável: Atendente
SE o Cliente Assinante solicitar Lavagem Simples ENTÃO informar que o serviço consome um uso do contador de Lavagens Completas, sem devolução de diferença de preço, e obter a confirmação verbal do cliente antes de abrir a Ordem de Serviço.

### Etapa 11 — Responsável: Atendente
SE o contador correspondente ao serviço solicitado for igual a zero ENTÃO informar ao cliente que o saldo do ciclo está esgotado e que o serviço será cobrado pelo preço cheio do Catálogo de Serviços como Serviço Excedente, e obter a confirmação verbal do cliente antes de abrir a Ordem de Serviço. SE o cliente não aceitar ENTÃO não iniciar o serviço e registrar a ocorrência no Registro de Anomalias.

### Etapa 12 — Responsável: Atendente
SE o Cliente Assinante solicitar Lavagem de Motor, Polimento, Higienização de Bancos ou Lavagem Detalhada ENTÃO classificar o serviço com Modalidade de Atendimento Avulso e cobrar o preço cheio do Catálogo de Serviços. Os Planos de Assinatura contemplam exclusivamente Lavagem Completa e Cera.

### Etapa 13 — Responsável: Atendente
SE a placa constar vinculada a Plano Inativo ENTÃO informar ao cliente que o plano está inativo por cobrança não liquidada, classificar todos os serviços com Modalidade de Atendimento Avulso e cobrar o preço cheio do Catálogo de Serviços. É proibido debitar Saldo de Serviços de Plano Inativo.

### Etapa 14 — Responsável: Atendente
SE o cliente solicitar Cera sem contratar Lavagem Simples ou Lavagem Completa na mesma visita ENTÃO verificar se o veículo está limpo o suficiente para receber a aplicação; SE não estiver ENTÃO informar ao cliente que a Cera exige lavagem prévia e oferecer a contratação da lavagem. É proibido aplicar Cera sobre veículo sujo.

### Etapa 15 — Responsável: Atendente
SE o cliente solicitar Lavagem Detalhada ENTÃO acionar o Gerente para elaborar o orçamento; SE o Gerente não estiver presente ENTÃO acionar o Colaborador mais experiente presente na unidade. Registrar o valor orçado e o escopo na Ordem de Serviço e obter a confirmação verbal do cliente antes de iniciar.

### Etapa 16 — Responsável: Atendente
Calcular o Tempo Prometido de Entrega somando os tempos-padrão de todos os serviços contratados para o veículo, conforme a Tabela de Tempos-Padrão, e acrescentando ao total o tempo de espera decorrente dos veículos já em fila. Os serviços são executados sequencialmente sobre o mesmo veículo, portanto seus tempos-padrão somam. Exemplo de cálculo: Lavagem de Motor, 60 minutos, mais Lavagem Completa, 60 minutos, mais Cera, 20 minutos, resultam em 140 minutos de execução, aos quais se soma a espera em fila. É proibido informar prazo por estimativa pessoal.

### Etapa 17 — Responsável: Atendente
Informar ao cliente o Tempo Prometido de Entrega em horário, e não em duração. Formato correto: informar que o veículo estará pronto às 14:30, e não que ficará pronto em uma hora e meia.

### Etapa 18 — Responsável: Atendente
Realizar a Vistoria de Entrada com o cliente presente ao lado do veículo, registrando na Ordem de Serviço: avarias visíveis em pintura, para-choques, rodas e vidros; nível de sujeira; e objetos aparentes no interior. É proibido receber a chave antes de concluir a Vistoria de Entrada.

### Etapa 19 — Responsável: Atendente
Solicitar ao cliente que retire do veículo objetos de valor, documentos e dinheiro antes da entrega da chave. SE o cliente optar por deixar objeto de valor no veículo ENTÃO registrar o objeto e sua localização na Ordem de Serviço.

### Etapa 20 — Responsável: Atendente
Abrir a Ordem de Serviço no Dashboard, preenchendo de forma obrigatória e antes do início de qualquer serviço: número, placa, modelo, cor, nome do cliente, telefone celular, serviços contratados, Modalidade de Atendimento de cada serviço, hora de entrada e Tempo Prometido de Entrega. SE o cliente recusar informar o telefone ENTÃO registrar a recusa e informá-lo de que não haverá aviso de conclusão do serviço.

### Etapa 21 — Responsável: Atendente
Receber a chave do cliente e pendurá-la imediatamente no gancho do Quadro de Chaves cujo número corresponda ao número da Ordem de Serviço. O número do gancho é o único vínculo entre o veículo no pátio e o seu registro no Dashboard. É proibido manter chave de cliente em bolso, sobre o capô, sobre o painel ou em qualquer posição que não seja o Quadro de Chaves.

### Etapa 22 — Responsável: Atendente
Definir o destino do veículo estritamente pela ordem de chegada. Não há prioridade de fila para nenhuma categoria de cliente, inclusive Cliente Assinante e Cliente de Conta Faturada.

### Etapa 23 — Responsável: Atendente
SE houver pedido de prioridade sobre a ordem de chegada ENTÃO encaminhar a decisão ao Proprietário, que é o único papel autorizado a conceder exceção, e registrar a exceção concedida no Registro de Anomalias.

### Etapa 24 — Responsável: Atendente
SE o veículo for de Cliente de Conta Faturada com retirada combinada para o fim do dia ENTÃO posicionar o veículo nas Vagas do Fundo. É proibido posicionar nas Vagas do Fundo qualquer veículo cujo Tempo Prometido de Entrega seja anterior ao horário de retirada do último veículo posicionado à sua frente, porque o Corredor de Acesso é único e obriga a remoção dos veículos da frente para liberar os do fundo.

### Etapa 25 — Responsável: Atendente
SE a capacidade disponível não permitir concluir os serviços dentro do horário de funcionamento do dia ENTÃO informar o cliente antes de receber a chave e registrar a ocorrência no Registro de Demanda Não Atendida com data, hora, placa quando disponível, categoria do cliente e motivo. Cliente Assinante pode ser recusado nas mesmas condições que as demais categorias; o serviço recusado não é debitado do Saldo de Serviços. Cabe ao Atendente avaliar e oferecer alternativa ao cliente quando houver.

### Etapa 26 — Responsável: Colaborador
Consultar a Ordem de Serviço no Dashboard antes de iniciar qualquer execução, identificando todos os serviços contratados para aquele veículo. É proibido iniciar a execução com base em instrução verbal sem conferência no Dashboard.

### Etapa 27 — Responsável: Colaborador
Executar os serviços contratados obrigatoriamente na Ordem de Execução dos Serviços: Lavagem de Motor, depois Lavagem Simples ou Lavagem Completa, depois Polimento, depois Cera, e por último Higienização de Bancos. É proibido alterar essa sequência.

### Etapa 28 — Responsável: Colaborador
Posicionar o veículo no Box de Lavagem de destino. SE houver veículo saindo pelo portão no mesmo momento ENTÃO aguardar a saída antes de iniciar a manobra, uma vez que o vão de 4,5 m do portão permite a passagem de um veículo por vez.

### Etapa 29 — Responsável: Colaborador
SE houver Lavagem de Motor contratada ENTÃO executá-la antes de qualquer outro serviço, aplicando desengraxante no compartimento do motor e enxaguando com máquina de alta pressão. A Lavagem de Motor precede a lavagem da carroceria porque a água e a sujeira do compartimento escorrem sobre a lataria.

### Etapa 30 — Responsável: Colaborador
Molhar o veículo integralmente com máquina de alta pressão, removendo barro e sujeira grossa antes de qualquer contato com a luva de lavagem.

### Etapa 31 — Responsável: Colaborador
Aplicar shampoo automotivo com luva de lavagem obrigatoriamente na seguinte ordem, de cima para baixo: teto; vidros; capô e tampa traseira; laterais e portas; para-choques e partes baixas; rodas e pneus por último.

### Etapa 32 — Responsável: Colaborador
É proibido retornar com a luva utilizada em rodas e pneus a qualquer superfície situada acima da linha inferior das portas. SE a luva tocar rodas ou pneus e for necessário retornar à carroceria ENTÃO substituir ou enxaguar integralmente a luva antes do retorno.

### Etapa 33 — Responsável: Colaborador
Enxaguar o veículo integralmente com máquina de alta pressão, de cima para baixo.

### Etapa 34 — Responsável: Colaborador
Secar o veículo com toalha, utilizando toalha exclusiva para vidros, distinta da toalha de carroceria. É proibido secar vidros com a toalha de carroceria.

### Etapa 35 — Responsável: Colaborador
Aplicar sopro de ar comprimido em frestas, retrovisores e maçanetas, e secar com toalha a água expelida por esse sopro. Registrar no Dashboard a conclusão da parte externa.

### Etapa 36 — Responsável: Colaborador
SE o serviço contratado for Lavagem Simples ENTÃO a execução da lavagem se encerra aqui e o veículo segue para o próximo serviço contratado ou para a Conferência Final; SE o serviço contratado for Lavagem Completa ENTÃO prosseguir para a etapa 37.

### Etapa 37 — Responsável: Colaborador
Retirar os tapetes do veículo e encaminhá-los imediatamente ao Ponto de Lavagem de Tapetes.

### Etapa 38 — Responsável: Colaborador
Deslocar o veículo do Box de Lavagem ao Ponto de Aspiração. SE houver veículo aguardando Box de Lavagem livre ENTÃO executar esse deslocamento antes de iniciar a limpeza interna, de modo a liberar o Box de Lavagem.

### Etapa 39 — Responsável: Colaborador
Aspirar bancos, assoalho e porta-malas, incluindo os cantos e os trilhos dos bancos.

### Etapa 40 — Responsável: Colaborador
Passar pano úmido em painel, console central e faces internas das portas.

### Etapa 41 — Responsável: Colaborador
Limpar os vidros pelo lado interno, obrigatoriamente após a limpeza de painel e console, e com pano distinto do utilizado no painel.

### Etapa 42 — Responsável: Colaborador
Recolocar os tapetes no veículo somente após a secagem completa. SE os tapetes não estiverem secos no momento da Conferência Final ENTÃO não liberar o veículo e registrar o motivo do atraso na Ordem de Serviço.

### Etapa 43 — Responsável: Colaborador
Aplicar pretinho nos quatro pneus e aplicar aromatizante na dosagem padrão. SE o cliente constar na Ficha de Preferências do Cliente com restrição de aroma ENTÃO aplicar a dosagem reduzida ali registrada. Registrar no Dashboard a conclusão da lavagem.

### Etapa 44 — Responsável: Colaborador
SE houver Polimento contratado ENTÃO deslocar o veículo do Box de Lavagem ao Container de Polimento após a conclusão da lavagem. O Polimento é executado no Container de Polimento e não ocupa Box de Lavagem.

### Etapa 45 — Responsável: Colaborador
SE houver Polimento contratado ENTÃO executá-lo com politriz sobre o veículo já lavado e seco, e registrar no Dashboard a conclusão. O Polimento ocupa 240 minutos do Colaborador que o executa, conforme a Tabela de Tempos-Padrão.

### Etapa 46 — Responsável: Colaborador
SE houver Cera contratada ENTÃO aplicá-la sobre o veículo lavado e seco, e obrigatoriamente após o Polimento quando este também tiver sido contratado, uma vez que a Cera é a camada de proteção aplicada sobre a pintura corrigida. Registrar no Dashboard a conclusão.

### Etapa 47 — Responsável: Colaborador
SE houver Higienização de Bancos contratada ENTÃO executá-la por último, depois de todos os demais serviços, utilizando o produto correspondente ao material do banco, couro ou tecido. Registrar no Dashboard a conclusão.

### Etapa 48 — Responsável: Colaborador
SE houver Higienização de Bancos contratada ENTÃO posicionar o veículo nas Vagas do Fundo até a secagem completa dos bancos. É proibido entregar veículo com banco úmido.

### Etapa 49 — Responsável: Colaborador
Consultar a Ficha de Preferências do Cliente no Dashboard antes de iniciar a Conferência Final. SE o cliente possuir Ficha de Preferências do Cliente ENTÃO verificar em primeiro lugar os pontos de atenção nela registrados.

### Etapa 50 — Responsável: Colaborador
Executar a Conferência Final em cem por cento dos veículos, sem exceção e sem amostragem, aplicando o Checklist de Conferência Final. A Conferência Final é executada pelo colaborador que concluiu o último serviço naquele veículo.

### Etapa 51 — Responsável: Colaborador
Verificar no Checklist de Conferência Final, no mínimo, os seguintes itens comuns a todo veículo: batentes das portas; porta-malas, incluindo forro e tampa; frestas, retrovisores e maçanetas sem água acumulada; vidros externos sem marcas; pretinho aplicado nos quatro pneus; ausência de avaria não registrada na Vistoria de Entrada.

### Etapa 52 — Responsável: Colaborador
Verificar itens adicionais conforme os serviços contratados. SE houver Lavagem Completa ENTÃO verificar também: vidros internos sem marcas; painel e console sem poeira; cantos e trilhos dos bancos; tapetes secos e recolocados; dosagem de aromatizante. SE houver Lavagem de Motor ENTÃO verificar ausência de resíduo de desengraxante e de água acumulada no compartimento. SE houver Cera ENTÃO verificar ausência de resíduo de cera em borrachas e frisos. SE houver Higienização de Bancos ENTÃO verificar secagem completa dos bancos.

### Etapa 53 — Responsável: Colaborador
SE todos os itens do Checklist de Conferência Final estiverem aprovados ENTÃO registrar a aprovação no Dashboard e liberar o veículo; SE houver item reprovado ENTÃO corrigir antes da liberação e registrar a ocorrência no Registro de Retrabalho, com data, placa, item reprovado, serviço de origem e colaborador responsável.

### Etapa 54 — Responsável: Colaborador
Posicionar o veículo aprovado na Vaga de Entrega. SE a Vaga de Entrega estiver com sua capacidade de 2 a 3 veículos ocupada ENTÃO posicionar o veículo nas Vagas do Fundo e acionar o Atendente para comunicar os clientes dos veículos que aguardam retirada.

### Etapa 55 — Responsável: Atendente
Comunicar ao cliente a conclusão do serviço imediatamente após a aprovação na Conferência Final, pelo WhatsApp corporativo, informando que o veículo deve ser retirado no prazo de 60 minutos contados do aviso. É proibido acumular avisos para envio posterior.

### Etapa 56 — Responsável: Atendente
SE o Tempo Prometido de Entrega for ultrapassado ENTÃO comunicar o cliente no momento em que o prazo for ultrapassado, informando o novo horário e o motivo. É proibido aguardar que o cliente descubra o atraso ao chegar na unidade.

### Etapa 57 — Responsável: Atendente
Realizar a entrega com o cliente presente, percorrendo com ele o exterior e o interior do veículo e conferindo em conjunto os itens registrados na Vistoria de Entrada.

### Etapa 58 — Responsável: Atendente
SE o cliente apontar item não conforme na entrega ENTÃO encaminhar o veículo ao Colaborador responsável para correção imediata, registrar a ocorrência no Registro de Retrabalho identificando que a detecção foi feita pelo cliente, e informar ao cliente o prazo de correção.

### Etapa 59 — Responsável: Atendente
Aplicar a cobrança por serviço, conforme a Modalidade de Atendimento registrada na Ordem de Serviço. SE a Modalidade for Assinatura ENTÃO não cobrar no ato e registrar o serviço para débito do Saldo de Serviços; SE a Modalidade for Conta Faturada ENTÃO não cobrar no ato e lançar na conta do cliente; SE a Modalidade for Avulso ou Excedente ENTÃO cobrar o preço cheio do Catálogo de Serviços, aceitando dinheiro, Pix ou cartão. Uma mesma Ordem de Serviço pode conter serviços em modalidades distintas, com parte debitada do plano e parte paga no ato.

### Etapa 60 — Responsável: Atendente
Registrar na Ordem de Serviço o valor cobrado por serviço, a forma de pagamento e a hora de saída do veículo. SE a Modalidade de Atendimento de um serviço for Assinatura ENTÃO registrar valor zero e a indicação de débito em plano.

### Etapa 61 — Responsável: Atendente
Devolver a chave ao cliente e dar baixa no gancho correspondente do Quadro de Chaves.

### Etapa 62 — Responsável: Responsável Administrativo
Debitar do Saldo de Serviços no Dashboard todo serviço registrado com Modalidade de Atendimento Assinatura, no prazo máximo de 3 dias úteis contados da conclusão do atendimento. Enquanto o débito não for lançado, o Dashboard exibe saldo superior ao real e a consulta da etapa 7 fica incorreta.

### Etapa 63 — Responsável: Responsável Administrativo
Não há suplência definida para o papel de Responsável Administrativo. SE o Responsável Administrativo estiver ausente por período que comprometa o prazo de 3 dias úteis ENTÃO os débitos permanecem pendentes até o seu retorno, e o Atendente deve considerar que o Saldo de Serviços exibido no Dashboard pode estar desatualizado.

### Etapa 64 — Responsável: Atendente
SE o cliente manifestar interesse em Plano de Assinatura, presencialmente ou pelo WhatsApp corporativo ENTÃO apresentar os três planos: Bronze, 129,99 reais, com 2 Lavagens Completas e 1 Cera; Prata, 229,99 reais, com 4 Lavagens Completas e 2 Ceras; Ouro, 259,99 reais, com 6 Lavagens Completas e 3 Ceras. Informar que os saldos são independentes, que expiram ao fim do Ciclo de Assinatura e que o plano é vinculado a uma placa fixa.

### Etapa 65 — Responsável: Atendente
Conduzir a adesão pela assinatura do Termo de Adesão vinculado ao Termo de Prestação de Serviço, na plataforma Portal Nogueira, registrando a placa do veículo a ser vinculada ao plano. O Ciclo de Assinatura inicia na data da assinatura do Termo de Adesão.

### Etapa 66 — Responsável: Atendente
SE o Cliente Assinante solicitar mudança de plano no curso do Ciclo de Assinatura ENTÃO cobrar a diferença integral entre o preço do plano atual e o do plano novo, ainda que o cliente venha a utilizar o plano novo por período inferior a 30 dias, e registrar a alteração no Portal Nogueira.

### Etapa 67 — Responsável: Responsável Administrativo
Atualizar a Ficha de Preferências do Cliente no Dashboard sempre que qualquer colaborador identificar exigência específica de cliente. É proibido manter exigência de cliente registrada apenas verbalmente ou apenas na memória de um colaborador.

### Etapa 68 — Responsável: Responsável Administrativo
Consolidar mensalmente o Registro de Retrabalho, o Registro de Demanda Não Atendida e o Registro de Anomalias, e apresentar a consolidação ao Proprietário, identificando os três itens de maior recorrência em cada registro e o número de Clientes Assinantes recusados no período.

### Etapa 69 — Responsável: Gerente
Acompanhar a execução dos serviços ao longo de todo o horário de funcionamento e verificar a conformidade da operação com este procedimento. O Gerente tem autoridade para redirecionar Colaboradores, redistribuir tarefas e interromper execução em desacordo com este procedimento.

### Etapa 70 — Responsável: Gerente
Cronometrar os tempos de execução dos Colaboradores por serviço e registrar os tempos aferidos no Dashboard. A cronometragem é a base de comparação entre o tempo real de execução e a Tabela de Tempos-Padrão prevista neste procedimento.

### Etapa 71 — Responsável: Gerente
SE o tempo real aferido de um serviço divergir de forma sistemática do valor previsto na Tabela de Tempos-Padrão ENTÃO propor ao Proprietário a recalibração do tempo daquele serviço, apresentando os tempos medidos que fundamentam a proposta. É proibido aplicar tempo diferente do previsto na Tabela de Tempos-Padrão antes da aprovação.

### Etapa 72 — Responsável: Proprietário
SE aprovar a recalibração proposta pelo Gerente ENTÃO a Tabela de Tempos-Padrão é alterada por revisão formal deste procedimento, com registro da alteração no Histórico de Revisões e definição de nova data de vigência. Até a publicação da revisão, permanece válida a tabela da versão vigente.

### Etapa 73 — Responsável: Gerente
Verificar por amostragem a qualidade dos veículos aprovados na Conferência Final, aplicando o Checklist de Conferência Final. SE identificar item reprovado em veículo já aprovado ENTÃO determinar o Retrabalho antes da entrega e registrar a ocorrência no Registro de Retrabalho, identificando que a detecção foi feita pelo Gerente.

### Etapa 74 — Responsável: Gerente
SE identificar desvio deste procedimento na execução ENTÃO corrigir o Colaborador no momento em que o desvio ocorrer. SE o mesmo desvio se repetir em dias distintos ENTÃO registrar a ocorrência no Registro de Anomalias e comunicar o Proprietário, para tratamento como falha de processo e não como falha individual.

### Etapa 75 — Responsável: Gerente
Apresentar mensalmente ao Proprietário a consolidação dos tempos aferidos por serviço e dos desvios recorrentes identificados, em conjunto com a consolidação dos registros elaborada pelo Responsável Administrativo.

## Ações em Caso de Anomalia
- SE o cliente afirmar possuir Saldo de Serviços divergente do exibido no Dashboard ENTÃO prevalece o registro do Dashboard para o atendimento em curso, o Atendente registra a divergência no Registro de Anomalias com placa, saldo alegado e saldo exibido, e encaminha ao Responsável Administrativo para verificação de débitos pendentes dentro do prazo de 3 dias úteis.
- SE o titular de Plano de Assinatura solicitar atendimento para veículo de placa distinta da cadastrada ENTÃO não debitar o Saldo de Serviços, informar que o plano é vinculado a placa fixa, tratar todos os serviços com Modalidade de Atendimento Avulso e cobrança pelo preço cheio, e registrar a ocorrência no Registro de Anomalias.
- SE o Cliente Assinante solicitar o cancelamento do Plano de Assinatura ENTÃO informar que não há reembolso proporcional e que o plano permanece ativo, com o Saldo de Serviços disponível, até o encerramento do Ciclo de Assinatura em curso, encaminhar a solicitação ao Proprietário e registrar a ocorrência no Registro de Anomalias.
- SE a cobrança recorrente de um Plano de Assinatura não for liquidada ENTÃO o plano passa imediatamente à condição de Plano Inativo, sem prazo de tolerância, o Saldo de Serviços deixa de estar disponível, e o cliente passa a ser atendido mediante pagamento do preço cheio do Catálogo de Serviços. Registrar a ocorrência no Registro de Anomalias.
- SE a chave de um veículo não for localizada no gancho do Quadro de Chaves ENTÃO o colaborador verifica primeiro o interior do veículo e os ganchos adjacentes; SE a chave não for localizada em 5 minutos ENTÃO comunicar o Proprietário, que assume a condução da busca. É proibido interromper todos os serviços em andamento para busca coletiva antes desse prazo. Registrar a ocorrência no Registro de Anomalias.
- SE um veículo for identificado parado na unidade sem Ordem de Serviço correspondente no Dashboard ENTÃO tratar o veículo como prioridade máxima sobre a fila, identificar o veículo pela placa, consultar a placa no Dashboard para restabelecer a condição de cobrança, abrir Ordem de Serviço registrando a hora de entrada como desconhecida, comunicar imediatamente o Proprietário, contatar o cliente informando a situação e o novo horário, e registrar a ocorrência no Registro de Anomalias.
- SE o número do gancho do Quadro de Chaves não corresponder a nenhuma Ordem de Serviço aberta no Dashboard ENTÃO identificar o veículo pela chave e pela placa, abrir a Ordem de Serviço faltante, corrigir a numeração do gancho e registrar a ocorrência no Registro de Anomalias. É proibido iniciar serviço em veículo cuja chave não esteja vinculada a Ordem de Serviço.
- SE o cliente apontar na entrega avaria não registrada na Vistoria de Entrada ENTÃO apresentar ao cliente o registro da Vistoria de Entrada daquele veículo no Dashboard e acionar o Proprietário, único papel autorizado a decidir sobre reparo, desconto ou isenção. Registrar a ocorrência no Registro de Anomalias com o desfecho adotado.
- SE o cliente relatar desaparecimento de objeto do interior do veículo ENTÃO apresentar ao cliente o registro de objetos aparentes feito na Vistoria de Entrada, acionar imediatamente o Proprietário, que conduz a apuração e a decisão, e registrar a ocorrência no Registro de Anomalias. É proibido a qualquer colaborador que não o Proprietário negociar ressarcimento com o cliente.
- SE um veículo aprovado na Conferência Final permanecer sem retirada por mais de 60 minutos contados do aviso de conclusão enviado ao cliente ENTÃO o Atendente contata o cliente pelo telefone cadastrado; SE o cliente não atender ENTÃO acionar o Colaborador para transferir o veículo às Vagas do Fundo, liberando a Vaga de Entrega, e registrar a ocorrência no Registro de Anomalias.
- SE um veículo não for retirado até o horário de encerramento do dia ENTÃO o Atendente contata o cliente antes do encerramento e informa que o veículo permanecerá na unidade, recolhe a chave ao Quadro de Chaves, e o Proprietário confere o fechamento do portão. Registrar a ocorrência no Registro de Anomalias.
- SE uma máquina de alta pressão apresentar falha durante a execução do serviço ENTÃO transferir o serviço para máquina de alta pressão disponível, sinalizar fisicamente a máquina com falha como fora de uso, comunicar o Proprietário no mesmo dia e registrar a ocorrência no Registro de Anomalias. É proibido manter em uso máquina que perca pressão durante a operação.
- SE houver menos de duas máquinas de alta pressão em condição de uso ENTÃO reduzir a alocação a dois Boxes de Lavagem simultâneos, revisar o Tempo Prometido de Entrega dos veículos em fila, comunicar os clientes afetados e registrar a ocorrência no Registro de Anomalias.
- SE começar a chover com veículo em etapa de lavagem externa ENTÃO concluir a etapa em Box de Lavagem coberto; SE não houver Box de Lavagem coberto disponível ENTÃO interromper a etapa, comunicar o cliente informando novo Tempo Prometido de Entrega, e registrar a ocorrência no Registro de Anomalias.
- SE as condições climáticas impedirem a secagem dos bancos após Higienização de Bancos dentro do Tempo Prometido de Entrega ENTÃO manter o veículo nas Vagas do Fundo, comunicar ativamente o cliente informando novo horário, e registrar a ocorrência no Registro de Anomalias. É proibido entregar veículo com banco úmido para cumprir prazo. O tempo-padrão da Higienização de Bancos já contempla a secagem em condições normais; a recorrência desta anomalia é indício de que o tempo-padrão precisa de recalibração pelo Gerente.
- SE a incidência direta de sol provocar secagem do produto sobre o veículo antes do enxágue ENTÃO transferir o veículo para Box de Lavagem coberto ou área sombreada antes de aplicar o shampoo; SE isso não for possível ENTÃO aplicar shampoo e enxaguar por seção do veículo, e não no veículo integralmente, de modo que nenhuma seção seque antes do enxágue.
- SE um colaborador faltar ENTÃO o Gerente redistribui as tarefas do dia mantendo obrigatoriamente coberto o papel de Atendente, reduz o número de Boxes de Lavagem simultâneos conforme a equipe disponível, revisa o Tempo Prometido de Entrega dos veículos em fila, e registra a ocorrência no Registro de Anomalias. A designação das tarefas do dia é atribuição do Gerente e não há suplência previamente designada.
- SE houver Polimento em execução e um colaborador faltar no mesmo dia ENTÃO o Gerente decide entre concluir o Polimento e reduzir a capacidade de lavagem, ou reagendar o Polimento com o cliente, uma vez que o Polimento ocupa 240 minutos do Colaborador que o executa. Registrar a decisão no Registro de Anomalias.
- SE o mesmo item reprovar na Conferência Final em três veículos distintos no mesmo dia ENTÃO o Colaborador que identificou a reprovação comunica o Gerente no mesmo dia, identificando o item e os Colaboradores envolvidos. O Gerente trata a ocorrência como falha de processo e não como falha individual, e comunica o Proprietário.
- SE o cliente solicitar serviço não previsto no Catálogo de Serviços ENTÃO o Atendente não assume o serviço e encaminha a solicitação ao Gerente, que a submete ao Proprietário, que decide sobre aceite, prazo e preço. É proibido acordar serviço, prazo ou preço fora deste procedimento sem decisão do Proprietário.

## Histórico de Revisões
- Versão 1.0 (Data: 29/07/2026, Autor: Equipe de consultoria — Insper Jr, 51ª Gestão): Versão inicial, elaborada a partir da transcrição da sessão de imersão com o Proprietário. Formalizou a jornada do veículo do portão à entrega e instituiu sete controles inexistentes: Vistoria de Entrada, campos obrigatórios de registro, sistema de duas vias em papel, uso obrigatório do Quadro de Chaves, Checklist de Conferência Final, Ficha de Preferências do Cliente e os registros de Retrabalho, de Demanda Não Atendida e de Anomalias. Não submetida a vigência.
- Versão 2.0 (Data: 30/07/2026, Autor: Equipe de consultoria — Insper Jr, 51ª Gestão): Alterou o horário de funcionamento para 08:00 às 17:00, de segunda a segunda. Incorporou os Planos de Assinatura em modelo de franquia única de lavagens, estabeleceu ordem de chegada estrita sem prioridade, atribuiu a Conferência Final ao colaborador que conclui o serviço e fixou os papéis por colaborador. Retirou do documento o tratamento de matérias jurídicas e societárias. Não submetida a vigência.
- Versão 3.0 (Data: 30/07/2026, Autor: Equipe de consultoria — Insper Jr, 51ª Gestão): Versão vigente. Elimina a comanda em papel e institui o Dashboard como sistema único de registro, com a Ordem de Serviço substituindo a comanda e o número do gancho do Quadro de Chaves como único vínculo entre o veículo no pátio e o seu registro digital. Incorpora o Catálogo de Serviços completo com preços fixos por serviço, iguais para qualquer porte de veículo. Estabelece a Ordem de Execução dos Serviços: Lavagem de Motor, lavagem, Polimento, Cera e Higienização de Bancos. Redefine os Planos de Assinatura como pacotes de dois contadores independentes, Bronze, Prata e Ouro, contemplando exclusivamente Lavagem Completa e Cera, com demais serviços cobrados a preço cheio. Institui a passagem imediata a Plano Inativo, o débito do Saldo de Serviços em até 3 dias úteis, e a venda e adesão de plano pelo Atendente via Portal Nogueira. Incorpora o Container de Polimento e as Vagas do Fundo à estrutura física. Substitui o cálculo do Tempo Prometido de Entrega por definição do Atendente, uma vez que a tabela de tempos-padrão depende de medição em operação real ainda não realizada. Define o acesso ao Dashboard por tablet no pátio, a janela de retirada de 60 minutos contados do aviso de conclusão, e não contempla procedimento de contingência para indisponibilidade do Dashboard, por decisão do Proprietário.
- Versão 3.1 (Data: 30/07/2026, Autor: Equipe de consultoria — Insper Jr, 51ª Gestão): Versão vigente. Elimina as denominações de função por posto: os papéis de Lavador e de Manobrista são substituídos pelo papel único de Colaborador, e o papel de Recepcionista de Pátio passa a ser denominado Atendente. Cria o papel de Gerente, com autoridade hierárquica sobre os Colaboradores, responsável pelo comando da operação do pátio, pela verificação de conformidade, pela cronometragem dos tempos de execução, pela verificação de qualidade por amostragem sobre veículos já aprovados na Conferência Final e pela redistribuição de tarefas. Transfere ao Gerente a elaboração do orçamento de Lavagem Detalhada, a redistribuição de tarefas em caso de falta de Colaborador e a decisão sobre Polimento em curso com equipe reduzida, mantendo com o Proprietário as decisões de isenção, desconto, reparo por conta da unidade e apuração de relato de desaparecimento de objeto. Corrige a data de elaboração de 30/07/2026 para 29/07/2026.
- Versão 3.2 (Data: 30/07/2026, Autor: Equipe de consultoria — Insper Jr, 51ª Gestão): Versão vigente. Institui a Tabela de Tempos-Padrão no corpo do procedimento, com os seguintes valores: Lavagem Simples, 20 minutos; Lavagem Completa, 60 minutos; Lavagem de Motor, 60 minutos; Polimento, 240 minutos; Cera, 20 minutos; Higienização de Bancos de couro, 120 minutos; Higienização de Bancos de tecido, 100 minutos. Os tempos de Higienização de Bancos já contemplam a secagem. A Lavagem Detalhada não possui tempo-padrão e tem o prazo definido no orçamento. Substitui a definição do Tempo Prometido de Entrega por estimativa do Atendente pelo cálculo objetivo da soma dos tempos-padrão dos serviços contratados acrescida da espera em fila, uma vez que os serviços são executados sequencialmente sobre o mesmo veículo. Estabelece que os tempos são médios e revisáveis conforme as cronometragens do Gerente, e que toda alteração da Tabela de Tempos-Padrão constitui revisão formal deste documento, proposta pelo Gerente, aprovada pelo Proprietário e registrada neste Histórico de Revisões. Corrige o tempo do Polimento, que deixa de ser descrito como consumo do dia inteiro do Colaborador e passa a 240 minutos, e o tempo da Higienização de Bancos, que passa a 120 minutos para couro e 100 minutos para tecido, com a secagem já incluída.
"""


@lru_cache()
def get_pop_documento() -> str:
    return _POP_DOCUMENTO
