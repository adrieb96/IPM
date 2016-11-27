package udc.fic.ipm;

import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.util.FloatMath;

public class ShakeDetector implements SensorEventListener{

	private static final float SHAKE_THRESHOLD_GRAVITY = 2.0F;
	private static final int SHAKE_SLOP_TIME_MS = 500;
	private static final int FACE_DOWN_MIN_TIME = 1500;
	private static final int MIN_TIME = 200;

	private OnShakeListener mListener;
	private long mShakeTimeStamp;
	private boolean mFaceDown = false;

	public void setOnShakeListener(OnShakeListener listener){
		this.mListener = listener;
	}

	public interface OnShakeListener{
		public void onShake();
		public void onFaceDown();
		public void onMovement();
	}

	@Override
	public void onAccuracyChanged(Sensor sensor, int accuracy){
		//ignore
	}

	@Override
	public void onSensorChanged(SensorEvent event){

		if(mListener != null){
			final long now = System.currentTimeMillis();
			
		/*	float rotation = 100;
			if(event.sensor.getType() == Sensor.TYPE_MAGNETIC_FIELD){
				mListener.onMovement();
				rotation = event.values[2];}
				*/

			float x = event.values[0];
			float y = event.values[1];
			float z = event.values[2];

			float gX = x / SensorManager.GRAVITY_EARTH;
			float gY = y / SensorManager.GRAVITY_EARTH;
			float gZ = z / SensorManager.GRAVITY_EARTH;

			float gForce = FloatMath.sqrt(gX*gX+gY*gY+gZ*gZ);

			/*
			//detect inclination
			if(rotation < 20 && rotation>-20){
				if(mFaceDown) return;
				
				mListener.onMovement();
				mShakeTimeStamp = now;
				mFaceDown = true;
				return;
			}

			if(mFaceDown && mShakeTimeStamp + FACE_DOWN_MIN_TIME < now){
				mFaceDown = false;
				mShakeTimeStamp = now;
				mListener.onFaceDown();
				return;
			}*/

			if(gForce > SHAKE_THRESHOLD_GRAVITY){
				if(mShakeTimeStamp + SHAKE_SLOP_TIME_MS > now) return;

				mShakeTimeStamp = now;

				mListener.onShake();

			}
		}
	}
}

