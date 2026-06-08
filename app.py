from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import sys
import os

# الحل: إضافة المسار الجذر للمشروع
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)  # إضافة المجلد الرئيسي

print(f"📁 Current directory: {current_dir}")
print(f"🔍 Looking for src in: {current_dir}")

# التحقق من وجود مجلد src وملفات __init__.py
src_path = os.path.join(current_dir, 'src')
pipeline_path = os.path.join(src_path, 'pipeline')
predict_file = os.path.join(pipeline_path, 'predict_pipeline.py')

print(f"📂 src exists: {os.path.exists(src_path)}")
print(f"📂 pipeline exists: {os.path.exists(pipeline_path)}")
print(f"📄 predict_pipeline.py exists: {os.path.exists(predict_file)}")
print(f"📄 src/__init__.py exists: {os.path.exists(os.path.join(src_path, '__init__.py'))}")

try:
    # جرب الاستيراد كباكج
    from src.pipeline.predict_pipeline import CustomData, PredictPipeline
    print("✅ Successfully imported from src.pipeline.predict_pipeline")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Trying alternative import...")
    
    # طريقة بديلة: استيراد مباشر
    import importlib.util
    
    spec = importlib.util.spec_from_file_location("predict_pipeline", predict_file)
    predict_module = importlib.util.module_from_spec(spec)
    sys.modules["predict_pipeline"] = predict_module
    spec.loader.exec_module(predict_module)
    
    CustomData = predict_module.CustomData
    PredictPipeline = predict_module.PredictPipeline
    print("✅ Successfully imported using importlib")

application = Flask(__name__)
app = application

@app.route('/')
def index():
    # Serve the prediction form at the root for convenience
    return render_template('home.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('race_ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=float(request.form.get('reading_score') or 0),
                writing_score=float(request.form.get('writing_score') or 0)
            )

            pred_df = data.get_data_as_data_frame()
            print("📊 DataFrame for prediction:")
            print(pred_df)

            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)

            return render_template('home.html', results=round(float(results[0]), 2))
        except Exception as e:
            return render_template('home.html', results=f"Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Flask application...")
    app.run(host="0.0.0.0", port=5000, debug=True)