#pylint: disable-all
from aw_nas.utils.torch_utils import random_cnn_data

def test_germ_resnet():
    from aw_nas.germ import GermSearchSpace
    from aw_nas.weights_manager.base import BaseWeightsManager

    ss = GermSearchSpace()
    wm = BaseWeightsManager.get_class_("germ")(
        ss, "cuda", rollout_type="germ",
        germ_supernet_type="nds_resnet",
        germ_supernet_cfg={
            "num_classes": 10,
            "stem_type": "res_stem_cifar"
        }
    )
    assert ss.get_size() == 1259712

    # ---- random sample and forward ----
    data = random_cnn_data(device="cuda", batch_size=2, input_c=3, output_c=10)
    for _ in range(5):
        rollout = ss.random_sample()
        cand_net = wm.assemble_candidate(rollout)
        outputs = cand_net(data[0])
        assert outputs.shape == (2, 10)
        print(rollout)
        print(outputs)

def test_germ_resnexta():
    from aw_nas.germ import GermSearchSpace
    from aw_nas.weights_manager.base import BaseWeightsManager

    ss = GermSearchSpace()
    wm = BaseWeightsManager.get_class_("germ")(
        ss, "cuda", rollout_type="germ",
        germ_supernet_type="nds_resnexta",
        germ_supernet_cfg={
            "num_classes": 10,
            "stem_type": "res_stem_cifar",
            "group_search": True
        }
    )
    assert ss.get_size() == 11390625

    # ---- random sample and forward ----
    data = random_cnn_data(device="cuda", batch_size=2, input_c=3, output_c=10)
    for _ in range(5):
        rollout = ss.random_sample()
        cand_net = wm.assemble_candidate(rollout)
        outputs = cand_net(data[0])
        assert outputs.shape == (2, 10)
        print(rollout)
        print(outputs)


    # sub search space without `num_groups` search
    ss_nogroup = GermSearchSpace()
    wm = BaseWeightsManager.get_class_("germ")(
        ss_nogroup, "cuda", rollout_type="germ",
        germ_supernet_type="nds_resnexta",
        germ_supernet_cfg={
            "num_classes": 10,
            "stem_type": "res_stem_cifar",
            "group_search": False
        }
    )
    assert ss_nogroup.get_size() == 421875 # no group
