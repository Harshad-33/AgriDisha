"""
PlantVillage 38-Class Plant Disease Information, Symptoms, Prevention, and Treatment Knowledge Base.
"""

DISEASE_CLASSES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

DISEASE_DETAILS = {
    'Apple___Apple_scab': {
        'crop': 'Apple',
        'disease': 'Apple Scab',
        'status': 'Diseased',
        'severity': 'Moderate to High',
        'cause': 'Fungus Venturia inaequalis',
        'symptoms': 'Olive-green to brown velvety spots on leaves and fruit, causing premature defoliation and cracked, deformed fruit.',
        'prevention': 'Rake and burn/compost fallen leaves in autumn, prune canopies for optimal air circulation, choose scab-resistant apple cultivars.',
        'treatment': 'Apply protective fungicide sprays such as Captan, Mancozeb, or Copper-based fungicides starting at green tip stage.',
        'supplement': 'Potassium silicate or organic neem oil extract.'
    },
    'Apple___Black_rot': {
        'crop': 'Apple',
        'disease': 'Black Rot',
        'status': 'Diseased',
        'severity': 'High',
        'cause': 'Fungus Botryosphaeria obtusa',
        'symptoms': 'Frog-eye leaf spots (purple margins with tan centers), black rotting mummified fruit, and branch cankers.',
        'prevention': 'Prune dead wood and remove mummified fruit from the orchard; sanitize pruning shears between cuts.',
        'treatment': 'Apply fungicides like Captan, Thiophanate-methyl, or Fludioxonil from petal fall through harvest.',
        'supplement': 'Balanced organic fertilizer with adequate calcium.'
    },
    'Apple___Cedar_apple_rust': {
        'crop': 'Apple',
        'disease': 'Cedar Apple Rust',
        'status': 'Diseased',
        'severity': 'Moderate',
        'cause': 'Fungus Gymnosporangium juniperi-virginianae',
        'symptoms': 'Bright orange or yellow-orange spots on the upper leaf surface; cup-shaped fungal structures underneath leaves.',
        'prevention': 'Remove nearby Eastern red cedar or juniper trees within 1-2 miles if possible; plant resistant apple varieties.',
        'treatment': 'Apply Myclobutanil, Mancozeb, or Triazole fungicides at blossom bud break.',
        'supplement': 'Foliar spray of kelp extract to boost systemic plant immunity.'
    },
    'Apple___healthy': {
        'crop': 'Apple',
        'disease': 'None (Healthy)',
        'status': 'Healthy',
        'severity': 'None',
        'cause': 'N/A',
        'symptoms': 'Vibrant, green, unblemished foliage with no fungal lesions or pest discoloration.',
        'prevention': 'Maintain regular watering schedule, balanced N-P-K fertilization, and periodic routine scouting.',
        'treatment': 'No fungicide needed. Maintain optimal orchard sanitation.',
        'supplement': 'Organic compost mulch and micronutrient foliar blend.'
    },
    'Blueberry___healthy': {
        'crop': 'Blueberry',
        'disease': 'None (Healthy)',
        'status': 'Healthy',
        'severity': 'None',
        'cause': 'N/A',
        'symptoms': 'Lush green leaves, robust shoots, and healthy acidic soil conditions (pH 4.5-5.5).',
        'prevention': 'Ensure proper soil acidity with elemental sulfur and adequate drip irrigation.',
        'treatment': 'No disease detected. Continue standard agronomic management.',
        'supplement': 'Acid-forming fertilizer (Ammonium sulfate) and pine bark mulch.'
    },
    'Cherry_(including_sour)___Powdery_mildew': {
        'crop': 'Cherry',
        'disease': 'Powdery Mildew',
        'status': 'Diseased',
        'severity': 'Moderate',
        'cause': 'Fungus Podosphaera clandestina',
        'symptoms': 'White powdery fungal coating on leaves and young shoots, causing leaf curling and distortion.',
        'prevention': 'Improve canopy airflow through judicious dormant pruning; avoid excessive nitrogen fertilization.',
        'treatment': 'Apply wettable sulfur, Potassium Bicarbonate, or Quinoxyfen at early signs of fungal colonies.',
        'supplement': 'Bio-fungicide containing Bacillus subtilis.'
    },
    'Cherry_(including_sour)___healthy': {
        'crop': 'Cherry',
        'disease': 'None (Healthy)',
        'status': 'Healthy',
        'severity': 'None',
        'cause': 'N/A',
        'symptoms': 'Glossy dark green leaves, vigorous shoot elongation, free of fungal powdery coatings or shot-holes.',
        'prevention': 'Prune annually during dry weather to maximize sun penetration and dry foliage.',
        'treatment': 'No disease treatment required.',
        'supplement': 'Balanced organic fruit tree fertilizer.'
    },
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': {
        'crop': 'Corn (Maize)',
        'disease': 'Gray Leaf Spot (Cercospora Leaf Spot)',
        'status': 'Diseased',
        'severity': 'High',
        'cause': 'Fungus Cercospora zeae-maydis',
        'symptoms': 'Rectangular, brown to gray lesions strictly bounded by leaf veins; blighting of upper canopy.',
        'prevention': 'Practice crop rotation away from corn for at least 1-2 years; bury crop residue with tillage.',
        'treatment': 'Foliar application of Strobilurin (Azoxystrobin) or Triazole (Pyraclostrobin) at tasseling stage (VT/R1).',
        'supplement': 'Potash and silicon soil amendments to enhance stalk strength.'
    },
    'Corn_(maize)___Common_rust_': {
        'crop': 'Corn (Maize)',
        'disease': 'Common Rust',
        'status': 'Diseased',
        'severity': 'Moderate',
        'cause': 'Fungus Puccinia sorghi',
        'symptoms': 'Small, cinnamon-brown to reddish pustules scattered across both upper and lower leaf surfaces.',
        'prevention': 'Plant rust-resistant hybrids; avoid late planting dates in humid regions.',
        'treatment': 'Apply fungicides (Propiconazole, Azoxystrobin, or Pyraclostrobin) if pustules appear before silking stage.',
        'supplement': 'Zinc and Boron micronutrient spray.'
    },
    'Corn_(maize)___Northern_Leaf_Blight': {
        'crop': 'Corn (Maize)',
        'disease': 'Northern Leaf Blight',
        'status': 'Diseased',
        'severity': 'High',
        'cause': 'Fungus Exserohilum turcicum',
        'symptoms': 'Long, elliptical, cigar-shaped grayish-green to tan lesions (1 to 6 inches long) on foliage.',
        'prevention': 'Use resistant hybrids with Ht genes; practice crop rotation and residue management.',
        'treatment': 'Apply systemic fungicides such as Pyraclostrobin + Fluxapyroxad or Azoxystrobin at early onset.',
        'supplement': 'Balanced N-P-K with sulfur.'
    },
    'Corn_(maize)___healthy': {
        'crop': 'Corn (Maize)',
        'disease': 'None (Healthy)',
        'status': 'Healthy',
        'severity': 'None',
        'cause': 'N/A',
        'symptoms': 'Robust, erect green stalks and wide arching green leaves with healthy ear development.',
        'prevention': 'Maintain balanced nitrogen top-dressing and optimal weed management.',
        'treatment': 'No disease treatment required.',
        'supplement': 'Zinc-enriched NPK 20-20-20.'
    },
    'Grape___Black_rot': {
        'crop': 'Grape',
        'disease': 'Black Rot',
        'status': 'Diseased',
        'severity': 'High',
        'cause': 'Fungus Guignardia bidwellii',
        'symptoms': 'Circular reddish-brown leaf spots with black fruiting bodies; berries shrivel into hard, black mummies.',
        'prevention': 'Prune out and destroy mummified grapes; open canopy for thorough sun penetration and rapid leaf drying.',
        'treatment': 'Apply Mancozeb, Captan, or Myclobutanil beginning when shoots are 2-4 inches long up to 4 weeks post-bloom.',
        'supplement': 'Copper hydroxide spray.'
    },
    'Grape___Esca_(Black_Measles)': {
        'crop': 'Grape',
        'disease': 'Esca (Black Measles)',
        'status': 'Diseased',
        'severity': 'Severe',
        'cause': 'Complex of Phaeomoniella chlamydospora & Fomitiporia mediterranea',
        'symptoms': 'Tiger-stripe leaf pattern (interveinal necrosis), dark spots on berries ("measles"), sudden vine apoplexy.',
        'prevention': 'Avoid pruning during wet periods; seal large pruning wounds with pruning paint/paste.',
        'treatment': 'No chemical cure exists for infected trunk wood; remove infected vines and renovate cordons.',
        'supplement': 'Trichoderma-based pruning wound protector.'
    },
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': {
        'crop': 'Grape',
        'disease': 'Leaf Blight (Isariopsis Leaf Spot)',
        'status': 'Diseased',
        'severity': 'Moderate',
        'cause': 'Fungus Pseudocercospora vitis',
        'symptoms': 'Irregular brown spots with dark borders that coalesce into large blighted areas, causing premature leaf drop.',
        'prevention': 'Improve vineyard drainage, ensure proper vine spacing, and practice regular leaf pulling.',
        'treatment': 'Spray Copper Oxychloride, Mancozeb, or Bordeaux mixture during humid conditions.',
        'supplement': 'Foliar potassium and zinc.'
    },
    'Grape___healthy': {
        'crop': 'Grape',
        'disease': 'None (Healthy)',
        'status': 'Healthy',
        'severity': 'None',
        'cause': 'N/A',
        'symptoms': 'Vibrant green canopy, healthy clusters, and vigorous cane growth free of fungal lesions.',
        'prevention': 'Maintain shoot thinning, cluster thinning, and timely irrigation control.',
        'treatment': 'No disease treatment required.',
        'supplement': 'Organic compost tea and sea kelp foliar.'
    },
    'Orange___Haunglongbing_(Citrus_greening)': {
        'crop': 'Orange (Citrus)',
        'disease': 'Huanglongbing (Citrus Greening)',
        'status': 'Diseased',
        'severity': 'Critical / Severe',
        'cause': 'Bacterium Candidatus Liberibacter asiaticus (vectored by Asian Citrus Psyllid)',
        'symptoms': 'Asymmetric blotchy mottled leaves, yellow shoots, small lopsided bitter green fruit with aborted seeds.',
        'prevention': 'Plant certified disease-free nursery stock; aggressively monitor and control Asian citrus psyllid vectors.',
        'treatment': 'No complete cure; control psyllid vector using Imidacloprid or Thiamethoxam; provide enhanced nutritional sprays.',
        'supplement': 'Foliar micronutrient cocktail (Zinc, Manganese, Iron, Boron) to sustain productive life.'
    },
    'Peach___Bacterial_spot': {
        'crop': 'Peach',
        'disease': 'Bacterial Spot',
        'status': 'Diseased',
        'severity': 'Moderate to High',
        'cause': 'Bacterium Xanthomonas arboricola pv. pruni',
        'symptoms': 'Water-soaked angular dark lesions on leaves that fall out giving a "shot-hole" look; cracked pitted fruit.',
        'prevention': 'Plant resistant peach varieties; avoid overhead irrigation; plant windbreaks to prevent sand-blasting injury.',
        'treatment': 'Apply copper bactericides during dormant/bud-swell stages and Oxytetracycline during growing season.',
        'supplement': 'Zinc sulfate dormant spray.'
    },
    'Peach___healthy': {
        'crop': 'Peach',
        'disease': 'None (Healthy)',
        'status': 'Healthy',
        'severity': 'None',
        'cause': 'N/A',
        'symptoms': 'Lush lanceolate foliage, strong new terminal shoots, smooth bark with no bacterial gummosis.',
        'prevention': 'Perform annual dormant pruning and maintain balanced nitrogen fertilization.',
        'treatment': 'No treatment required.',
        'supplement': 'Boron and calcium foliar sprays during flowering.'
    },
    'Pepper,_bell___Bacterial_spot': {
        'crop': 'Pepper (Bell)',
        'disease': 'Bacterial Spot',
        'status': 'Diseased',
        'severity': 'High',
        'cause': 'Bacterium Xanthomonas campestris pv. vesicatoria',
        'symptoms': 'Small, circular, dark water-soaked spots with yellow halos on leaves; raised scabby lesions on fruits.',
        'prevention': 'Use certified pathogen-free seed and resistant hybrids; disinfect seed trays; avoid overhead sprinkling.',
        'treatment': 'Spray preventive Copper Hydroxide mixed with Mancozeb; apply Actigard (systemic acquired resistance inducer).',
        'supplement': 'Streptomycin sulfate (where permitted) or bio-bactericide (Bacillus subtilis).'
    },
    'Pepper,_bell___healthy': {
        'crop': 'Pepper (Bell)',
        'disease': 'None (Healthy)',
        'status': 'Healthy',
        'severity': 'None',
        'cause': 'N/A',
        'symptoms': 'Glossy dark green leaves, sturdy stems, abundant flowering and firm bell pepper fruit set.',
        'prevention': 'Mulch beds to conserve moisture and maintain even calcium availability to prevent blossom-end rot.',
        'treatment': 'No disease treatment required.',
        'supplement': 'Calcium-magnesium (Cal-Mag) booster.'
    },
    'Potato___Early_blight': {
        'crop': 'Potato',
        'disease': 'Early Blight',
        'status': 'Diseased',
        'severity': 'Moderate to High',
        'cause': 'Fungus Alternaria solani',
        'symptoms': 'Dark brown to black target-board concentric ring spots on older leaves, surrounded by chlorotic yellow halos.',
        'prevention': 'Maintain optimal plant vigor with balanced nitrogen; rotate with non-solanaceous crops for 2-3 years.',
        'treatment': 'Apply protective fungicides like Chlorothalonil, Mancozeb, or Azoxystrobin when conditions favor blight.',
        'supplement': 'Potassium-rich foliar feed to reduce physiological stress.'
    },
    'Potato___Late_blight': {
        'crop': 'Potato',
        'disease': 'Late Blight',
        'status': 'Diseased',
        'severity': 'Critical',
        'cause': 'Oomycete Phytophthora infestans',
        'symptoms': 'Dark water-soaked lesions that turn necrotic rapidly; white fuzzy fungal growth on underside of leaves in humid weather.',
        'prevention': 'Plant certified disease-free seed tubers; eliminate cull piles; avoid sprinkler irrigation late in the day.',
        'treatment': 'Apply systemic oomycete fungicides like Metalaxyl (Ridomil Gold), Cymoxanil, Fluopicolide, or Mancozeb.',
        'supplement': 'Copper-based preventative spray.'
    },
    'Potato___healthy': {
        'crop': 'Potato',
        'disease': 'None (Healthy)',
        'status': 'Healthy',
        'severity': 'None',
        'cause': 'N/A',
        'symptoms': 'Healthy sprawling green foliage, crisp unblemished leaflets, vigorous underground tuber bulking.',
        'prevention': 'Hill soil around plants properly to prevent tuber greening and spore wash-off.',
        'treatment': 'No disease treatment required.',
        'supplement': 'Phosphorus and Potash tuber bulking fertilizer.'
    },
    'Raspberry___healthy': {
        'crop': 'Raspberry',
        'disease': 'None (Healthy)',
        'status': 'Healthy',
        'severity': 'None',
        'cause': 'N/A',
        'symptoms': 'Deep green trifoliate leaves, healthy floricanes/primocanes with no spur blight or anthracnose.',
        'prevention': 'Prune out old floricanes right after harvest; ensure high trellis airflow.',
        'treatment': 'No disease treatment required.',
        'supplement': 'Organic compost and composted bark mulch.'
    },
    'Soybean___healthy': {
        'crop': 'Soybean',
        'disease': 'None (Healthy)',
        'status': 'Healthy',
        'severity': 'None',
        'cause': 'N/A',
        'symptoms': 'Lush green trifoliate foliage, vigorous nodulation on roots, healthy pod development.',
        'prevention': 'Ensure Bradyrhizobium japonicum inoculation at planting and proper drainage.',
        'treatment': 'No disease treatment required.',
        'supplement': 'Molybdenum and Boron seed treatment.'
    },
    'Squash___Powdery_mildew': {
        'crop': 'Squash',
        'disease': 'Powdery Mildew',
        'status': 'Diseased',
        'severity': 'Moderate',
        'cause': 'Fungus Podosphaera xanthii',
        'symptoms': 'White powdery talcum-like spots covering upper and lower leaf surfaces, leading to early leaf senescence.',
        'prevention': 'Select powdery mildew resistant squash varieties; plant in full sun with generous spacing.',
        'treatment': 'Apply Potassium Bicarbonate, Neem Oil, Wettable Sulfur, or Myclobutanil at earliest signs.',
        'supplement': 'Diluted milk spray (40% milk / 60% water) as an organic photo-activated antifungal.'
    },
    'Strawberry___Leaf_scorch': {
        'crop': 'Strawberry',
        'disease': 'Leaf Scorch',
        'status': 'Diseased',
        'severity': 'Moderate',
        'cause': 'Fungus Diplocarpon earlianum',
        'symptoms': 'Numerous small, irregular purple to dark brown spots that expand and coalesce, giving leaves a scorched appearance.',
        'prevention': 'Plant disease-free crowns; avoid excessive nitrogen fertilizer which stimulates lush susceptible tissue.',
        'treatment': 'Apply fungicides like Captan, Pyraclostrobin, or Copper Hydroxide after spring renovation or at first spots.',
        'supplement': 'Bio-stimulant with mycorrhizae and sea minerals.'
    },
    'Strawberry___healthy': {
        'crop': 'Strawberry',
        'disease': 'None (Healthy)',
        'status': 'Healthy',
        'severity': 'None',
        'cause': 'N/A',
        'symptoms': 'Lush glossy green runners, bright white flowers with golden centers, and firm unspotted berries.',
        'prevention': 'Mulch with clean straw to keep berries off bare soil; remove dead leaves during winter.',
        'treatment': 'No disease treatment required.',
        'supplement': 'Balanced organic berry food (3-4-4).'
    },
    'Tomato___Bacterial_spot': {
        'crop': 'Tomato',
        'disease': 'Bacterial Spot',
        'status': 'Diseased',
        'severity': 'Moderate to High',
        'cause': 'Bacterium Xanthomonas perforans / euvesicatoria',
        'symptoms': 'Small, water-soaked brown spots with yellow halos on leaves; raised, blister-like spots on green tomatoes.',
        'prevention': 'Use disease-free seed; clean stakes and trellises; avoid overhead watering; rotate crops with non-solanaceous plants.',
        'treatment': 'Apply Copper Hydroxide paired with Mancozeb; apply bacteriophages (AgriPhage) or Actigard SAR inducer.',
        'supplement': 'Bacillus amyloliquefaciens microbial inoculant.'
    },
    'Tomato___Early_blight': {
        'crop': 'Tomato',
        'disease': 'Early Blight',
        'status': 'Diseased',
        'severity': 'Moderate to High',
        'cause': 'Fungus Alternaria linariae (Alternaria solani)',
        'symptoms': 'Dark brown concentric "bullseye" rings on bottom leaves, yellowing of surrounding tissue, progressing upward.',
        'prevention': 'Prune lower leaves touching soil; stake and cage plants; apply mulch around base; rotate crops for 3 years.',
        'treatment': 'Apply Chlorothalonil, Copper Fungicide, or Mancozeb every 7-10 days starting at bottom foliage.',
        'supplement': 'Liquid kelp and potassium silicate foliar.'
    },
    'Tomato___Late_blight': {
        'crop': 'Tomato',
        'disease': 'Late Blight',
        'status': 'Diseased',
        'severity': 'Critical / Severe',
        'cause': 'Oomycete Phytophthora infestans',
        'symptoms': 'Large, irregular water-soaked greasy gray spots turning brown-black; white fungal mildew under leaves; rot on fruit.',
        'prevention': 'Plant resistant varieties (e.g. Defiant, Mountain Merit); destroy infected plants immediately; ensure wide spacing.',
        'treatment': 'Apply preventative Chlorothalonil or Copper. At early onset, use Curzate (Cymoxanil) or Revus (Mandipropamid).',
        'supplement': 'Phosphorous acid salts (e.g. Agri-Fos).'
    },
    'Tomato___Leaf_Mold': {
        'crop': 'Tomato',
        'disease': 'Leaf Mold',
        'status': 'Diseased',
        'severity': 'Moderate',
        'cause': 'Fungus Passalora fulva (Cladosporium fulvum)',
        'symptoms': 'Pale green to yellowish spots on upper leaf surface with olive-brown velvety fungal mold underneath.',
        'prevention': 'Common in greenhouse settings; lower relative humidity below 85% with exhaust fans and ventilation.',
        'treatment': 'Apply Copper fungicides, Chlorothalonil, or Azoxystrobin; remove heavily infected lower leaves.',
        'supplement': 'Air circulation fans and drip irrigation lines.'
    },
    'Tomato___Septoria_leaf_spot': {
        'crop': 'Tomato',
        'disease': 'Septoria Leaf Spot',
        'status': 'Diseased',
        'severity': 'Moderate',
        'cause': 'Fungus Septoria lycopersici',
        'symptoms': 'Numerous small, circular spots (1-3mm) with dark brown borders and grayish-white centers with tiny black specks.',
        'prevention': 'Mulch around stems to stop fungal spores splashing from soil; clean garden debris in fall.',
        'treatment': 'Apply Chlorothalonil, Copper octanoate, or Mancozeb on a 7-14 day schedule.',
        'supplement': 'Compost tea and organic fish fertilizer.'
    },
    'Tomato___Spider_mites Two-spotted_spider_mite': {
        'crop': 'Tomato',
        'disease': 'Spider Mites (Two-Spotted Spider Mite)',
        'status': 'Diseased (Pest Infestation)',
        'severity': 'Moderate to High',
        'cause': 'Mite Tetranychus urticae',
        'symptoms': 'Fine yellow speckling (stippling) on upper leaf surface, fine silken webbing on undersides of leaves.',
        'prevention': 'Keep plants well hydrated as drought stress favors mites; spray water on undersides of leaves to knock off mites.',
        'treatment': 'Apply insecticidal soap, Neem oil, Horticultural mineral oil, or release predatory mites (Phytoseiulus persimilis).',
        'supplement': 'Wettable sulfur (do not apply within 30 days of oil sprays).'
    },
    'Tomato___Target_Spot': {
        'crop': 'Tomato',
        'disease': 'Target Spot',
        'status': 'Diseased',
        'severity': 'Moderate',
        'cause': 'Fungus Corynespora cassiicola',
        'symptoms': 'Small brown circular lesions with light brown centers and dark concentric rings; dark sunken lesions on fruit.',
        'prevention': 'Maintain wide plant spacing for airflow; avoid overhead watering; prune suckers and lower leaf skirts.',
        'treatment': 'Apply Azoxystrobin, Chlorothalonil, or Famoxadone + Cymoxanil.',
        'supplement': 'Humic acid and calcium foliar boost.'
    },
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': {
        'crop': 'Tomato',
        'disease': 'Yellow Leaf Curl Virus (TYLCV)',
        'status': 'Diseased',
        'severity': 'Severe',
        'cause': 'Begomovirus transmitted by Whiteflies (Bemisia tabaci)',
        'symptoms': 'Severe stunting, erect bushy growth, leaves curled upward with prominent yellow margins and reduced fruit set.',
        'prevention': 'Use TYLCV-resistant hybrids; install 50-mesh insect screens in greenhouses; deploy yellow sticky traps for whiteflies.',
        'treatment': 'No chemical cure for viral infections; eradicate infected plants immediately; manage whitefly vectors with Pyriproxyfen or Spiromesifen.',
        'supplement': 'Neem oil or insecticidal soap for vector control.'
    },
    'Tomato___Tomato_mosaic_virus': {
        'crop': 'Tomato',
        'disease': 'Tomato Mosaic Virus (ToMV)',
        'status': 'Diseased',
        'severity': 'Severe',
        'cause': 'Tobamovirus (mechanically transmitted)',
        'symptoms': 'Mottled light and dark green mosaic patterns on leaves, fern-leaf distortion, internal browning in fruit.',
        'prevention': 'Wash hands and disinfect tools with 20% skim milk solution or 10% bleach; smokers must wash hands before handling plants.',
        'treatment': 'No chemical cure exists. Remove and destroy infected plants; avoid composting diseased residues.',
        'supplement': 'Plant resistant cultivars labeled Tm-2 or Tm-2^2.'
    },
    'Tomato___healthy': {
        'crop': 'Tomato',
        'disease': 'None (Healthy)',
        'status': 'Healthy',
        'severity': 'None',
        'cause': 'N/A',
        'symptoms': 'Deep green, sturdy foliage, thick stems, vibrant yellow blossoms, and developing unblemished tomatoes.',
        'prevention': 'Maintain consistent watering, cage supports, clean mulch layer, and periodic scouting.',
        'treatment': 'No disease treatment required.',
        'supplement': 'Calcium-rich organic tomato fertilizer (5-10-10) with bone meal.'
    }
}


def get_disease_info(class_name: str) -> dict:
    """Retrieve full advisory details for a given disease class."""
    if class_name in DISEASE_DETAILS:
        return DISEASE_DETAILS[class_name]
    
    # Fallback parsing
    parts = class_name.split('___')
    crop_name = parts[0].replace('_', ' ')
    disease_name = parts[1].replace('_', ' ') if len(parts) > 1 else 'Unknown'
    is_healthy = 'healthy' in disease_name.lower()
    
    return {
        'crop': crop_name,
        'disease': disease_name if not is_healthy else 'None (Healthy)',
        'status': 'Healthy' if is_healthy else 'Diseased',
        'severity': 'None' if is_healthy else 'Moderate',
        'cause': 'N/A' if is_healthy else 'Agricultural pathogen',
        'symptoms': 'Healthy plant foliage.' if is_healthy else 'Visible abnormal lesions or discoloration on foliage.',
        'prevention': 'Follow standard crop management guidelines and maintain hygiene.',
        'treatment': 'No treatment necessary.' if is_healthy else 'Inspect carefully and apply appropriate organic/chemical treatment.',
        'supplement': 'Balanced organic fertilizer.'
    }
