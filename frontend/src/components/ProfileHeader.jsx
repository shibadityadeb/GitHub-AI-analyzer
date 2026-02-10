import { MapPin, Briefcase, Link as LinkIcon, Calendar, Users, Code } from 'lucide-react';

export default function ProfileHeader({ profile }) {
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long'
    });
  };

  return (
    <div className="card">
      <div className="flex items-start space-x-6">
        {/* Avatar */}
        <img
          src={profile.avatar_url}
          alt={profile.login}
          className="w-24 h-24 rounded-full border-4 border-blue-100"
        />

        {/* Profile Info */}
        <div className="flex-1">
          <div className="flex items-start justify-between mb-3">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">
                {profile.name || profile.login}
              </h2>
              <a
                href={`https://github.com/${profile.login}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline"
              >
                @{profile.login}
              </a>
            </div>
            
            {profile.hireable && (
              <span className="badge badge-success">
                Available for hire
              </span>
            )}
          </div>

          {profile.bio && (
            <p className="text-gray-700 mb-4">{profile.bio}</p>
          )}

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            {profile.location && (
              <div className="flex items-center space-x-2 text-gray-600">
                <MapPin className="w-4 h-4" />
                <span>{profile.location}</span>
              </div>
            )}
            
            {profile.company && (
              <div className="flex items-center space-x-2 text-gray-600">
                <Briefcase className="w-4 h-4" />
                <span>{profile.company}</span>
              </div>
            )}
            
            {profile.blog && (
              <div className="flex items-center space-x-2 text-gray-600">
                <LinkIcon className="w-4 h-4" />
                <a
                  href={profile.blog.startsWith('http') ? profile.blog : `https://${profile.blog}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-blue-600 truncate"
                >
                  {profile.blog.replace(/^https?:\/\//, '')}
                </a>
              </div>
            )}
            
            <div className="flex items-center space-x-2 text-gray-600">
              <Calendar className="w-4 h-4" />
              <span>Joined {formatDate(profile.created_at)}</span>
            </div>
          </div>

          <div className="flex items-center space-x-6 mt-4 text-sm">
            <div className="flex items-center space-x-2">
              <Code className="w-4 h-4 text-gray-500" />
              <span className="font-semibold text-gray-900">{profile.public_repos}</span>
              <span className="text-gray-600">repositories</span>
            </div>
            <div className="flex items-center space-x-2">
              <Users className="w-4 h-4 text-gray-500" />
              <span className="font-semibold text-gray-900">{profile.followers}</span>
              <span className="text-gray-600">followers</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-gray-900">{profile.following}</span>
              <span className="text-gray-600">following</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
