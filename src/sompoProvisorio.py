from src.db import conexao

import re
from datetime import datetime


def insertDados(sql, values):
    conn = conexao.myConexao()
    cursor = conn.cursor()
    res = cursor.execute(sql, values)

    cursor.close()
    conn.commit()
    conn.close()
    if res == 1:
        return True
    else:
        return False


def obterPrecos(driver):
    site = 'http://localhost:63342/SimuladorOnline/src/html/sompo-rj.html?_ijt=v0gaae7eiko1makm9vg4o34st2'
    driver.get(site)
    planos_atualizados = []
    planos_sem_cadastros = []
    planos_inseridos = []
    salvar = conexao.inserirRegistro()
    atualizarPreco = conexao.updatePrecoPlano()
    inseridos = 0

    id_operadora = 12
    id_area = 4

    try:
        num = 1

        while True:

            try:
                refTable = driver.find_element_by_xpath(f'//*[@id="tab-produto"]/div/h4[{num}]')
            except:
                print("element no ionterable")
                refTable = False
                break
            finally:
                pass

            titulo = driver.find_element_by_xpath(f'//*[@id="tab-produto"]/div/h4[{num}]').text
            validade = driver.find_element_by_xpath(f'//*[@id="tab-produto"]/div/p[{num}]').text
            print(f"\nLendo {num}")
            print(titulo)
            print(validade)

            titulo = str(titulo).upper()
            qtd_titulares = '1'
            hospitalar = 1
            min_vidas = None
            max_vidas = None
            if re.search('03 A 29 VIDAS', titulo):
                min_vidas = 0
                max_vidas = 29
            elif re.search('30 A 99 VIDAS', titulo):
                min_vidas = 30
                max_vidas = 0

            if re.search("HOSPITALAR", titulo):
                hospitalar = 2

            if re.search("SEM COPAR", titulo):
                id_coparticipacao = 2
            elif re.search('20%', titulo):
                id_coparticipacao = 3
            elif re.search('30%', titulo):
                id_coparticipacao = 5

            if re.search("COMPULSÓRIO", titulo):
                id_tipo_contratacao = 2
            else:
                id_tipo_contratacao = 1


            planos = driver.find_element_by_xpath(
                f'//*[@id="tab-produto"]/div/table[{num}]/thead').find_elements_by_tag_name('th')

            planosArray = []
            for plano in planos:
                planosArray.append(plano.text)

            # del(planosArray[0])
            print(planosArray)

            for i, plano in enumerate(planosArray):
                # print("num",i)
                precos = []
                for j in range(10):
                    if i > 0:
                        preco = driver.find_element_by_xpath(
                            f'//*[@id="tab-produto"]/div/table[{num}]/tbody/tr[{j + 1}]/td[{i + 1}]').text
                        precos.append(float(str(preco).replace(".", "").replace(",", ".")))

                if i > 0:
                    print(precos)

                    nomePlano = str(plano).split('[')
                    plano = nomePlano[0].strip().upper()
                    modalidade = nomePlano[1].split(']')[0].strip()
                    id_modalidade = 0

                    if modalidade == "E":
                        id_modalidade = 1

                        if plano == "CLASSICO":
                            plano = "CLÁSSICO ENF"

                    elif modalidade == "A":
                        id_modalidade = 2

                        if plano == "CLASSICO":
                            plano = "CLÁSSICO APT"

                    conn = conexao.myConexao()
                    cursor = conn.cursor()

                    sql = f"SELECT * FROM tbl_tipo_plano where titulo like '{plano}' and id_operadora = {id_operadora};"
                    print(sql)
                    res = cursor.execute(sql)
                    # print(res)
                    if res == 1:
                        result_select = cursor.fetchall()[0]
                        print(result_select)
                        id_plano = result_select[0]
                        id_categoria_plano = result_select[3]

                        id_tipo_empresa = 2
                        id_administradora = 0
                        data_reajuste = '2021-06-15'
                        id_tipo_contratacao_lead = 0
                        id_tipo_tabela = None

                        print("id_area => ", id_area)
                        print("id_categoria_plano => ", id_categoria_plano)
                        print("id_coparticipacao => ", id_coparticipacao)
                        print("id_modalidade => ", id_modalidade)
                        print("id_operadora => ", id_operadora)
                        print("id_tipo_contratacao => ", id_tipo_contratacao)
                        print("id_plano => ", id_plano)
                        print("preco0_18 => ", precos[0])
                        print("preco_m59 => ", precos[9])
                        print("qtd_titulares => ", qtd_titulares)
                        print("hospitalar => ", hospitalar)
                        print("min_vidas => ", min_vidas)
                        print("max_vidas => ", max_vidas)
                        print("id_tipo_empresa => ", id_tipo_empresa)
                        print("id_administradora => ", id_administradora)
                        print("data_reajuste => ", data_reajuste)
                        print("id_tipo_contratacao_lead => ", id_tipo_contratacao_lead)
                        print("id_tipo_tabela => ", id_tipo_tabela)

                        sql = "insert into tbl_preco_faixa_etaria (" \
                              "id_area, " \
                              "id_categoria_plano, " \
                              "id_coparticipacao, " \
                              "id_modalidade, " \
                              "id_operadora, " \
                              "id_tipo_contratacao, " \
                              "id_tipo_plano, " \
                              "preco0_18, " \
                              "preco19_23, " \
                              "preco24_28, " \
                              "preco29_33, " \
                              "preco34_38, " \
                              "preco39_43, " \
                              "preco44_48, " \
                              "preco49_53, " \
                              "preco54_58, " \
                              "preco_m59, " \
                              "qtd_titulares, " \
                              "id_sindicato, " \
                              "hospitalar, " \
                              "min_vidas, " \
                              "max_vidas, " \
                              "id_tipo_empresa, " \
                              "id_administradora, " \
                              "ultimo_reajuste, " \
                              "id_tipo_contratacao_lead, " \
                              "id_tipo_tabela ) " \
                              "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

                        values = (
                            id_area,  # id_area
                            id_categoria_plano,  # id_categoria_plano
                            id_coparticipacao,  # id_coparticipacao
                            id_modalidade,  # id_modalidade,
                            id_operadora,  # id_operadora
                            id_tipo_contratacao,  # id_tipo_contratacao
                            id_plano,  # id_tipo_plano
                            precos[0],  # preco0_18
                            precos[1],  #
                            precos[2],
                            precos[3],
                            precos[4],
                            precos[5],
                            precos[6],
                            precos[7],
                            precos[8], # preco54_58
                            precos[9],
                            qtd_titulares,  # qtd_titulares
                            None,  # id_sindicato
                            hospitalar,  # hospitalar
                            min_vidas,  # min_vidas
                            max_vidas,  # max_vidas
                            id_tipo_empresa,  # id_tipo_empresa
                            id_administradora,  # id_administradora
                            data_reajuste,  # ultimo_reajuste
                            id_tipo_contratacao_lead,  # id_tipo_contratacao_lead
                            id_tipo_tabela  # id_tipo_tabela
                        )
                        # print(values)

                        teste = "select * from tbl_preco_faixa_etaria " \
                                f"where id_area = {id_area} " \
                                f"and id_operadora = {id_operadora} " \
                                f"and id_tipo_plano = {id_plano} " \
                                f"and id_modalidade = {id_modalidade} " \
                                f"and id_tipo_contratacao = {id_tipo_contratacao} " \
                                f"and id_coparticipacao = {id_coparticipacao} " \
                                f"and qtd_titulares = {qtd_titulares} " \
                                f"and min_vidas = {min_vidas} " \
                                f"and id_sindicato is null " \
                                f"and id_tipo_empresa = {id_tipo_empresa} " \
                                f"and hospitalar = {hospitalar};"
                        print(teste)
                        res = cursor.execute(teste)

                        print(values, " -- extraidos do simulador")
                        if res == 1:
                            select = cursor.fetchall()[0]
                            id = select[0]
                            preco0_18 = select[8]
                            preco59 = select[17]
                            ultimo_reajuste = select[25]

                            print(select[1:28], f"ID: {id} -- banco de dados")
                            if not preco0_18 == precos[0] or not preco59 == precos[9]:  # and not ultimo_reajuste == data_reajuste
                                print("Atualizar Precos! -----")
                                planos_atualizados.append(plano)

                                if ultimo_reajuste == None:
                                    ultimo_reajuste = "null"
                                else:
                                    ultimo_reajuste = datetime.strptime(str(ultimo_reajuste), '%Y-%m-%d').date()
                                print(ultimo_reajuste)

                                update = "UPDATE `tbl_preco_faixa_etaria` SET " \
                                         f"`preco0_18`='{precos[0]}', " \
                                         f"`preco19_23`='{precos[1]}', " \
                                         f"`preco24_28`='{precos[2]}', " \
                                         f"`preco29_33`='{precos[3]}', " \
                                         f"`preco34_38`='{precos[4]}', " \
                                         f"`preco39_43`='{precos[5]}', " \
                                         f"`preco44_48`='{precos[6]}', " \
                                         f"`preco49_53`='{precos[7]}', " \
                                         f"`preco54_58`='{precos[8]}', " \
                                         f"`preco_m59`='{precos[9]}', " \
                                         f"`min_vidas`='{min_vidas}', " \
                                         f"`max_vidas`='{max_vidas}', " \
                                         f"`ultimo_reajuste`='{data_reajuste}' " \
                                         f"WHERE `id`='{id}';"
                                print(update)

                                if atualizarPreco:
                                    res = cursor.execute(update)
                                else:
                                    res = 1

                                if res == 1:

                                    if ultimo_reajuste == None or ultimo_reajuste == "null":
                                        insert = "insert into tbl_historico_precos_planos " \
                                                 "(id_preco_faixa_etaria, preco0_18, preco19_23, preco24_28, preco29_33, preco34_38, preco39_43, preco44_48, preco49_53, preco54_58, preco_m59 ) " \
                                                 "values " \
                                                 f"({id}, {select[8]}, {select[9]}, {select[10]}, {select[11]}, {select[12]}, {select[13]}, {select[14]}, {select[15]}, {select[16]}, {select[17]}); "
                                    else:
                                        insert = "insert into tbl_historico_precos_planos " \
                                                 "(id_preco_faixa_etaria, preco0_18, preco19_23, preco24_28, preco29_33, preco34_38, preco39_43, preco44_48, preco49_53, preco54_58, preco_m59, data_validade) " \
                                                 "values " \
                                                 f"({id}, {select[8]}, {select[9]}, {select[10]}, {select[11]}, {select[12]}, {select[13]}, {select[14]}, {select[15]}, {select[16]}, {select[17]}, '{ultimo_reajuste}'); "

                                    print(insert)
                                    if salvar:
                                        res = cursor.execute(insert)
                                        print(res, "sucesso")

                        elif res == 0:
                            print("----------------------------- Cadastrar Novo --------------------------------")
                            print(f'{sql} {values}')
                            ref_plano = True
                            for plan in planos_inseridos:
                                if plan == plano:
                                    ref_plano = False

                            if ref_plano:
                                planos_inseridos.append(f"{plano}")

                            if salvar:

                                if not insertDados(sql, values):
                                    print("ERROR: erro ao inserir precos no banco de dados!")
                                else:
                                    inseridos += 1
                        elif res > 1:
                            print("Mais de um plano cadastrado")

                    # Colocar em uma lista os planos nao encontrados
                    elif res == 0:
                        print("Nao achou o plano!")
                        ref_plano = True
                        for plan in planos_sem_cadastros:
                            if plan == plano:
                                ref_plano = False

                        if ref_plano:
                            planos_sem_cadastros.append(f"{plano}")
                    elif res > 1:
                        print("Achou mais de um plano!")

                    cursor.close()
                    conn.commit()
                    conn.close()

            num += 1




    # except:
    #     print("Acabou")
    #     # pass
    finally:
        pass
    print(f"Total de preços de planos atualizados: {inseridos}")
    # print(f"Planos que nao foram encontrados: \n {planos_sem_cadastros}")
    # print(f"Planos que sofreram alteracoes: \n {planos_atualizados}")
    # print(f"Planos sem preços cadastrados: \n {planos_inseridos}")