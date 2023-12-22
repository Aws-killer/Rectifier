import {Composition} from 'remotion';
import {HelloWorld} from './HelloWorld';
import Constants from './HelloWorld/Assets/Constants.json';
import './index.css';
export const RemotionRoot = () => {
	return (
		<>
			<Composition
				id="HelloWorld"
				component={HelloWorld}
				durationInFrames={Constants?.dutaion ? Constants.duration : 60 * 30}
				fps={30}
				height={Constants?.height ? Constants.height : 1920}
				width={Constants?.width ? Constants.width : 1080}
			/>
		</>
	);
};
