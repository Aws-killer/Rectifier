import {Composition} from 'remotion';
import {HelloWorld} from './HelloWorld';
import {DURATION} from './HelloWorld/constants';
import 'index.css';
export const RemotionRoot = () => {
	return (
		<>
			<Composition
				id="HelloWorld"
				component={HelloWorld}
				durationInFrames={DURATION}
				fps={30}
				height={1920}
				width={1080}
			/>
		</>
	);
};
