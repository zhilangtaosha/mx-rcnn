from gluoncv.data import VOCDetection, COCODetection
from gluoncv.utils.metrics import VOC07MApMetric, COCODetectionMetric


class VOC:
    def __init__(self, is_train):
        self._ds_cls = VOCDetection
        self._mt_cls = VOC07MApMetric
        self._imageset = '2007_trainval' if is_train else '2007_test'

    def set_args(self, args):
        args.rcnn_num_classes = len(self._ds_cls.CLASSES) + 1

    def get_dataset(self, imageset):
        imageset = imageset if imageset else self._imageset
        splits = [(int(s.split('_')[0]), s.split('_')[1]) for s in imageset.split('+')]
        return self._ds_cls(splits=splits)

    def get_metric(self, dataset):
        return self._mt_cls(iou_thresh=0.5, class_names=dataset.classes)

    def get_names(self):
        return self._ds_cls.CLASSES


class COCO:
    def __init__(self, is_train):
        self._is_train = is_train
        self._ds_cls = COCODetection
        self._mt_cls = COCODetectionMetric
        self._imageset = 'instances_train2017' if is_train else 'instances_val2017'

    def set_args(self, args):
        args.img_short_side = 800
        args.img_long_side = 1333
        args.rpn_anchor_scales = (2, 4, 8, 16, 32)
        args.rcnn_num_classes = len(self._ds_cls.CLASSES) + 1

    def get_dataset(self, imageset):
        imageset = imageset if imageset else self._imageset
        splits = imageset.split('+')
        return self._ds_cls(splits=splits, skip_empty=self._is_train)

    def get_metric(self, dataset):
        return self._mt_cls(dataset, save_prefix='coco', cleanup=True)

    def get_names(self):
        return self._ds_cls.CLASSES


DATASETS = {
    'voc': VOC,
    'coco': COCO
}


def get_dataset_train(ds_name, args):
    if ds_name not in DATASETS:
        raise ValueError("dataset {} not supported".format(ds_name))
    ds = DATASETS[ds_name](is_train=True)
    ds.set_args(args)
    dataset = ds.get_dataset(args.imageset)
    return dataset


def get_dataset_test(ds_name, args):
    if ds_name not in DATASETS:
        raise ValueError("dataset {} not supported".format(ds_name))
    ds = DATASETS[ds_name](is_train=False)
    ds.set_args(args)
    dataset = ds.get_dataset(args.imageset)
    metric = ds.get_metric(dataset)
    return dataset, metric


def get_dataset_demo(ds_name, args):
    if ds_name not in DATASETS:
        raise ValueError("dataset {} not supported".format(ds_name))
    ds = DATASETS[ds_name](is_train=False)
    ds.set_args(args)
    names = ds.get_names()
    return names
