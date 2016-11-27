package udc.fic.ipm;

import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.util.FloatMath;

public class ShakeDetector implements SensorEventListener{

	private static final float SHAKE_THRESHOLD_GRAVITY = 2.5F;
	private static final int SHAKE_SLOP_TIME_MS = 2000;
	private static final int FACE_DOWN_MIN_TIME = 1500;
	private static final int ROTATION_MAX_TIME = 1000;
	private static final int MIN_TIME = 200;

	private OnShakeListener mListener;
	private long mShakeTimeStamp;
	private long timeToFlip;
	private boolean mFaceDown = false;
	private int mCountFlip = 0;

	public void setOnShakeListener(OnShakeListener listener){
		this.mListener = listener;
	}

	private Orientation orientation = Orientation.VER;

	private enum Orientation{
		HOR,VER
	};

	public interface OnShakeListener{
		public void onShake();
		public void onFaceDown();
		public void onMovement();
		public void onMovement(String str);
		public void onRotation();
	}

	@Override
	public void onAccuracyChanged(Sensor sensor, int accuracy){
		//ignore
	}

	public Boolean isHorizontal(float n){
		return !isVertical(n);
	}

	public boolean isVertical(float n){
		return (n>-15 && n<20);
	}

	@Override
	public void onSensorChanged(SensorEvent event){

		if(mListener != null){
			final long now = System.currentTimeMillis();
		
			if(event.sensor.getType() == Sensor.TYPE_MAGNETIC_FIELD){
				float rotation = event.values[2];
				float flip = event.values[1];
				
				if(rotation < 20 && rotation>-20){
					if(mFaceDown) return;
					mShakeTimeStamp = now;
					mFaceDown = true;
					return;
				}
				
				if(mFaceDown && mShakeTimeStamp + FACE_DOWN_MIN_TIME < now){
					mShakeTimeStamp = now;
					mFaceDown = false;
					mListener.onFaceDown();
					return;
				}
				if(mFaceDown) return;
				
				if(isHorizontal(flip) && orientation.equals(Orientation.VER)){
					mListener.onMovement("HORIZONTAL");
					if(mCountFlip<1) timeToFlip = now;
					mCountFlip++;
					orientation = Orientation.HOR;
					mListener.onMovement("FLIPS " + mCountFlip);
					return;
				}

				if(mCountFlip==0) {
					orientation = Orientation.VER;
					return;
				}
				
				if(isVertical(flip) && orientation.equals(Orientation.HOR)){
					mListener.onMovement("VERTICAL");
					mCountFlip++;
					orientation = Orientation.VER;
					mListener.onMovement("FLIPS " + mCountFlip);
				}

				if(timeToFlip + ROTATION_MAX_TIME < now){
					mListener.onMovement("TIME : " + (timeToFlip - now));
					timeToFlip = now;
					mCountFlip=0; 
					return;
				}

				if(mCountFlip>2){
					mListener.onRotation();
					mCountFlip = 0;
					return;
				}
			}	

			if(event.sensor.getType() == Sensor.TYPE_ACCELEROMETER){
				float x = event.values[0];
				float y = event.values[1];
				float z = event.values[2];

				float gX = x / SensorManager.GRAVITY_EARTH;
				float gY = y / SensorManager.GRAVITY_EARTH;
				float gZ = z / SensorManager.GRAVITY_EARTH;

	
				float gForce = FloatMath.sqrt(gX*gX+gY*gY+gZ*gZ);

				if(gForce > SHAKE_THRESHOLD_GRAVITY){
					if(mShakeTimeStamp + SHAKE_SLOP_TIME_MS > now) return;

					mShakeTimeStamp = now;

					mListener.onShake();
				}
			}
		}
	}
}

