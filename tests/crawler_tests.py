from nose.tools import *
from autodl.crawler import *
import os

def create_fake_conf(tmp_file):
    with open(tmp_file, "w") as file_tmp:
        json.dump({"supported_sites":{"animes":["mangaFrCom", "animeserv"], "series":["scenesources", "telechargementz"]}, "target_titles":{"animes":{"naruto": "None", "shoukugeki": "9"}, "series":{"atlantis": "10", "olympus": "None"}},"target_ep":{"shoukugeki": "9","atlantis": "10"}}, file_tmp)

def delete_fake_conf(tmp_file):
    os.remove(tmp_file)

def test_targets():
    tmp_file = "/tmp/conf_tmp.json"
    create_fake_conf(tmp_file)

    tgt = Targets(config_file=tmp_file)
    assert_equal(tgt.config_file_path, tmp_file)

    delete_fake_conf(tmp_file)

def test_is_valid_type():
    tmp_file = "/tmp/conf_tmp.json"
    create_fake_conf(tmp_file)

    tgt = Targets(config_file=tmp_file)
    val = tgt.is_valid_type("animes")
    assert_equal(val, True)

    val2 = tgt.is_valid_plugin("theater")
    assert_equal(val2, False)

    delete_fake_conf(tmp_file)

def test_is_valid_site():
    tmp_file = "/tmp/conf_tmp.json"
    create_fake_conf(tmp_file)

    tgt = Targets(config_file=tmp_file)
    val = tgt.is_valid_plugin("mangaFrCom")
    assert_equal(val, True)

    val2 = tgt.is_valid_plugin("test")
    assert_equal(val2, False)

    delete_fake_conf(tmp_file)

def test_ep_to_dl():
    tmp_file = "/tmp/conf_tmp.json"
    create_fake_conf(tmp_file)

    tgt = Targets(config_file=tmp_file)
    val = tgt.ep_to_dl("animes", "shoukugeki")
    assert_equal(val, "9")

    delete_fake_conf(tmp_file)

def test_targets_create():
    tmp_file = "/tmp/conf_tmp.json"
    create_fake_conf(tmp_file)

    tgt = Targets(config_file=tmp_file)
    # Test with no arguments provided
    lt = tgt.create()
    #print lt
    assert_equal(lt[0][0], "series")
    assert_equal(lt[0][1], "scenesources")
    assert_equal(lt[0][2], "atlantis")
    assert_equal(lt[0][3], "10")
    # If 1 argument is provided
    lt = tgt.create(target_type="animes")
    #print lt
    assert_equal(lt[0][0], "animes")
    assert_equal(lt[0][1], "mangaFrCom")
    assert_equal(lt[0][2], "naruto")
    assert_equal(lt[0][3], "None")
    # Test with 2 arguments
    lt = tgt.create(target_type="animes", target_site="animeserv")
    #print lt
    assert_equal(lt[0][0], "animes")
    assert_equal(lt[0][1], "animeserv")
    assert_equal(lt[0][2], "naruto")
    # Test with 3 arguments
    lt = tgt.create(target_type="animes", target_site="animeserv", target_title="claymore")
    #print lt
    assert_equal(lt[0][0], "animes")
    assert_equal(lt[0][1], "animeserv")
    assert_equal(lt[0][2], "claymore")

    delete_fake_conf(tmp_file)
