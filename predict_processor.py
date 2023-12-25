   # import craft functions
from craft_text_detector import (
    read_image,
    load_craftnet_model,
    load_refinenet_model,
    get_prediction,
    export_detected_regions,
    export_extra_results,
    empty_cuda_cache
)


def craft_text_detector(image, refine_net, craft_net):
 

    # set image path and export folder directory
    # image = './IMG_3529.JPG' # can be filepath, PIL image or numpy array
    output_dir = './craft_result/'
    shutil.rmtree('./craft_result/image_crops') 



    # read image
    image = read_image(image)

    
    # perform prediction
    prediction_result = get_prediction(
        image=image,
        craft_net=craft_net,
        refine_net=refine_net,
        text_threshold=0.5,
        link_threshold=0.7,
        low_text=0.4,
        cuda=False,
        long_size=1280   )
    
    height, width, channels  = image.shape

    boxes = prediction_result["boxes"]
    # for box in boxes:
    #     box[0][1] = max(0, box[0][1]-25)
    #     box[1][1] = max(0, box[1][1]-25)
    #     box[2][1] = min(height, box[2][1]+25)
    #     box[3][1] = min(height, box[3][1]+25)
    lines = []
    line = []
    for box in boxes:
        if len(line) == 0:
            line.append(box)
        else:
            last_word = line[-1]
            mid_y = (box[2][1]+ box[0][1])/2
            if mid_y > last_word[2][1] or mid_y < last_word[0][1]:
                lines.append(line)
                line = []
            line.append(box)
    if len(line)> 0 :
        lines.append(line)

    sorted_lines = [sorted(i, key = lambda x:x[0][0]) for i in lines ]
    final_lines = []
    for i in sorted_lines:
        for j in i:
            final_lines.append(j)
    
    # export detected text regions
    exported_file_paths = export_detected_regions(
        image=image,
        regions=final_lines,
        output_dir=output_dir,
        rectify=True
    )

    # export heatmap, detection points, box visualization
    export_extra_results(
        image=image,
        regions=boxes,
        heatmaps=prediction_result["heatmaps"],
        output_dir=output_dir
    )
import matplotlib.pyplot as plt
from PIL import Image

from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import glob
import shutil 


def vietocr_text_recognition(image ):
    craft_text_detector(image, craft_refine_net, craft_net)
    config = Cfg.load_config_from_name('vgg_transformer')
    config['weights'] = './weights/transformerocr.pth'
    config['cnn']['pretrained']=False
    config['predictor']['beamsearch']=False

    config['vocab'] = 'aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ ƒ'

    dataset_params = {
        'name':'hw',
        'data_root':'./data_line/',
        'train_annotation':'train_annotation.txt',
        'valid_annotation':'test_annotation.txt',
        'image_height':32
    }

    params = {
            'print_every':200,
            'valid_every':1000,
            'iters':25000,
            'checkpoint':'./checkpoint/transformerocr_checkpoint.pth',
            'export':'./weights/transformerocr.pth',
            'metrics': 5000,
            'batch_size': 16
            }

    config['trainer'].update(params)
    config['dataset'].update(dataset_params)
    config['device'] = 'cpu'
    detector = Predictor(config)

    image_paths = glob.glob('./craft_result/image_crops/*.png')
    image_paths.sort(key=lambda x: [len(x), x])
    result = []
    print("before")
    for img in image_paths:
        img = Image.open(img)
        s = detector.predict(img)
        result.append(s)
    print(result)
    for i in result:
        print(i, end = ' ')
    return result

from datetime import datetime




image = './user_img/IMG_3529.JPG'
# load models
craft_refine_net = load_refinenet_model(cuda=False)
craft_net = load_craftnet_model(cuda=False, weight_path='./craft_mlt_25k.pth')
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
# vietocr_text_recognition(image)
# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# print("Current Time =", current_time)
